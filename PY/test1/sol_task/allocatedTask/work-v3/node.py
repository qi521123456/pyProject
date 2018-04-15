try:
    from queue import Queue
    from enum import Enum
    from kazoo.client import KazooClient
    import subprocess
    import threading
    import os,socket
    import logging,logging.handlers
    import time
    import psutil
    import pickle
except ImportError as IE:
    print(IE)
    exit()
class Utils:
    @classmethod
    def localAddr(cls):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            mac = ''
            for k, v in psutil.net_if_addrs().items():
                if k == 'docker0':
                    for item in v:
                        address = item[1]
                        if len(address) == 17:
                            mac = address
                            break
        except:
            ip = '局域网地址ipv4'
            mac = 'docker0 mac地址'
            print('can`t get ip and mac')
            sys.exit(0)
        return str(ip),str(mac)
    @classmethod
    def localPath(cls):
        path = os.path.split(os.path.realpath(__file__))[0]
        return path
class Env:
    PATH = Utils.localPath()
    IP,Docker0_MAC = Utils.localAddr()
    DockerNum = 5   # 默认最多5个docker同时运行，启动项目时可更改
    DOCKER = 'scan:v2'
    ZookeeperHost = '192.168.205.27'
    task_topic = '/taskmgt/task'
    result_topic = '/taskmgt/result'
    node_topic = '/node/status'
    province_src = PATH+'/province/'
    local_result_path = PATH+'/result/'
    if not os.path.exists(local_result_path):
        os.makedirs(local_result_path)
    if not os.path.exists(province_src):
        os.makedirs(province_src)
    target_result_path = "root@192.168.120.30:/home/lmq"  #  TODO 需要ssh免密登录
    log = PATH+'/logs/node-'+IP+'.log'
class Logging:
    def __init__(self,path):
        self.logger = logging.getLogger()
        self.shandler = logging.StreamHandler()
        file_dir = path[:path.rfind('/')]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.fhandler = logging.handlers.RotatingFileHandler(path,maxBytes=10*1024*1024,backupCount=3)  #  3份日志滚动，每个10M
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.shandler.setFormatter(self.formatter)
        self.fhandler.setFormatter(self.formatter)
        self.logger.addHandler(self.shandler)
        self.logger.addHandler(self.fhandler)
        return self.logger
g_logger = Logging(Env.log).get_logger()
class Task:
    def __init__(self,task_id, task_strategy, scan_ip, scan_province, scan_nodes, scan_port, protocol, script):
        self.task_id = task_id  # str
        self.task_strategy = task_strategy # str
        if scan_ip == "":
            self.scan_ip = None
        else:
            self.scan_ip = scan_ip # list []
        self.scan_province = scan_province # str
        self.scan_nodes = scan_nodes # list []
        self.scan_port = scan_port # int | str
        if scan_port is None:
            self.scan_port = protocol.get('protocolPort')
        self.protocol = protocol # dict {'protocolName':xxx,'portType':TCP|UDP}
        self.script = script # bytes b'xxxxxxxx'

class TaskPkl:
    def __init__(self,taskid,scantype,port,script,pct,white):
        self.taskid = taskid
        self.scantype = scantype
        self.port = port
        self.script = script
        self.pct = pct  # tcp or udp
        self.white = white
class TaskResult:
    def __init__(self,taskID,taskStatus,taskResult,message):
        self.task_id = str(taskID)
        self.task_status = str(taskStatus)
        self.result_name = str(taskResult)
        self.message = message
    def __str__(self):
        return str(self.__dict__)
class Docker:
    def __init__(self,name,process,taskid):
        self.dockerName = name
        self.work_path = Env.PATH+'/'+name+'/'
        if not os.path.exists(self.work_path):
            os.makedirs(self.work_path)
        self.process = process
        self.taskid = str(taskid)
class NodeStatus:
    def __init__(self):
        self.msg_type = "node_status"
        self.nodeIP = Env.IP
        self.docker_sum = Env.DockerNum
        self.run_docker_num = len(TaskMgt.docker_list)
        self.nodeDetail = {
            'cpu': str(psutil.cpu_percent())+'%',
            'tStorage': str(psutil.disk_usage("/").total/(1024*1024)) + 'M',
            'uStorage': str(psutil.disk_usage("/").used/(1024*1024)) + 'M'
        }
    def __str__(self):
        return str(self.__dict__)

class TaskStatus(Enum):
    INIT = "init"
    RUNNING = "running"
    DONE = "done"
class Strategy(Enum):
    PORT = 'port_scan'
    PROTOCOL = 'protocol_sniffer'

class TaskMgt:
    task_queue = Queue(maxsize=0)
    docker_list = set()

class Consumer:
    def __init__(self,taskmgt):
        self.taskmgt = taskmgt

    def __get_command(self, task_env,docker_name,pkl_file):
        # docker run --env hostip=192.168.120.6 --env mac=02:42:11:46:a0:6d --env docker=docker2 -v /home/lmqdcs:/home/lmqdcs scan:v2 python3 /home/lmqdcs/v2/scan.py /home/lmqdcs/v2/pkl1.pkl
        scan_script = Env.PATH + "/scan.py"
        hostip = 'hostip=%s'%Env.IP
        mac = 'mac=%s'%Env.Docker0_MAC
        env_doc = 'docker=%s'%docker_name
        share_path = '%s:%s'%(Env.PATH,Env.PATH)
        command = ['docker','run','--env',hostip,'--env',mac,'--env',env_doc,'-v',share_path,Env.DOCKER,'python3',scan_script,pkl_file]
        return command

    def __get_target(self, file_name, factor, seq):
        '''
        省份扫描 ip分片
        :param file_name:
        :param factor:
        :param seq:
        :return:
        '''
        with open(file_name,encoding='UTF-8') as f:
            lines = f.readlines()
        targets = []
        try:
            if (factor-seq) is 1:
                targets = lines[seq * (len(lines) // factor):len(lines)]
            else:
                targets = lines[seq * len(lines) // factor : (seq+1) * len(lines) // factor]
        except RuntimeError:
            pass
        return targets

    def consume(self):
        taskmgt = self.taskmgt
        while True:
            if taskmgt.task_queue.empty() or len(taskmgt.docker_list) >= Env.DockerNum:
                time.sleep(5)
                continue
            try:
                docker_name = None
                for i in range(1,Env.DockerNum+1):
                    isinflag = False
                    docker_name = "docker"+str(i)
                    for run_doc in taskmgt.docker_list:
                        if docker_name == run_doc.dockerName:
                            isinflag = True
                            break
                    if not isinflag:
                        break
                if docker_name is None:
                    continue
                task = taskmgt.task_queue.get()
                scan_ip = task.scan_ip
                scan_province = task.scan_province
                task_env = Env.PATH + '/'+docker_name + '/'
                if not os.path.exists(task_env):
                    os.makedirs(task_env)
                ip_file = task_env + 'white.txt'
                if scan_ip is not None and scan_ip != '':
                    scan_targets = scan_ip
                else:
                    scan_nodes = task.scan_nodes
                    province_src = Env.province_src + scan_province + ".txt"  # 若扫描省份，一次只能扫一个
                    scan_targets = self.__get_target(province_src, len(scan_nodes), scan_nodes.index(Env.IP))
                with open(ip_file,'w',encoding='UTF-8') as opener:
                    for target in scan_targets:
                        opener.write(str(target).strip()+'\n')
                scantype = None
                script_file = ''
                pct = ''
                if task.task_strategy == Strategy.PROTOCOL.value:
                    scantype = 'protocol'
                    script_file = task_env + task.protocol.get('protocolName') + ".nse"
                    if task.protocol.get('portType') == 'TCP':
                        pct = 'sS'
                    else:
                        pct = 'sU'
                    with open(script_file, 'w', encoding='UTF-8') as writer:
                        writer.write(task.script)
                elif task.task_strategy == Strategy.PORT.value:
                    scantype = 'port'
                pkl_file = task_env+'.task.pkl'
                task_pkl = TaskPkl(task.task_id,scantype,task.scan_port,script_file,pct,ip_file)
                with open(pkl_file,'wb') as fw:
                    pickle.dump(task_pkl,fw)
                cmd = self.__get_command(task_env,docker_name,pkl_file)
                g_logger.info('begin task: %s, %s'%(task.task_id," ".join(cmd)))
                child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
                taskmgt.docker_list.add(Docker(docker_name,child,task.task_id))
            except Exception as ex:
                g_logger.info(ex)

class Monitor:
    def __init__(self,taskmgt):
        self.taskmgt = taskmgt
    def __scheduler(self, message):
        try:

            task = Task(message.get('taskId'), message.get('scanStrategy'), message.get('scanIp'),
                        message.get('province'), message.get('scanNodes'), message.get('scanPort'),
                        message.get('protocol'), message.get('script'))
            self.taskmgt.task_queue.put(task)

        except Exception as ex:
            g_logger.error(ex)
            return
    def docker_moniter(self):
        '''
        更新docker——list状态,并收集扫描结果scp至主节点
        :return:
        '''
        zk_client.set(Env.result_topic, str("{'message':'flush'}").encode())
        while True:
            if len(self.taskmgt.docker_list)>0:
                for run_docker in list(self.taskmgt.docker_list):  # 必要转换
                    run_docker.process.poll()  # 不能少
                    zip_file_name = run_docker.taskid + '-' + run_docker.dockerName + '@' + Env.IP
                    if run_docker.process.returncode == 0:
                        self.taskmgt.docker_list.remove(run_docker)
                        g_logger.info('task : %s is over' % run_docker.taskid)
                        scp_cmd = 'scp %s %s'%(Env.local_result_path+zip_file_name+'.zip',Env.target_result_path)
                        try:
                            os.system(scp_cmd)
                            g_logger.info('scp over : %s' % scp_cmd)
                            os.system("rm -f %s" % Env.local_result_path+zip_file_name+'.zip')
                            task_res = TaskResult(run_docker.taskid,TaskStatus.DONE.value,zip_file_name,'success')
                        except Exception as e:
                            g_logger.error('scp error : %s ' % scp_cmd)
                            g_logger.error(e)
                            task_res = TaskResult(run_docker.taskid, TaskStatus.DONE.value, zip_file_name, 'error:scp wrong')
                    else:
                        task_res = TaskResult(run_docker.taskid, TaskStatus.RUNNING.value, zip_file_name, 'success')
                    zk_client.set(Env.result_topic,str(task_res).encode())
                    zk_client.set(Env.result_topic, str("{'message':'flush'}").encode())
                    time.sleep(1)
            time.sleep(1)
    def node_status(self):
        while True:
            time.sleep(5)
            node_status = NodeStatus()
            zk_client.set(Env.node_topic,str(node_status).encode())
    def monitor(self):
        thread_consumer = threading.Thread(target=Consumer(self.taskmgt).consume)
        thread_docker = threading.Thread(target=self.docker_moniter)
        thread_node = threading.Thread(target=self.node_status)
        thread_consumer.start()
        thread_docker.start()
        thread_node.start()
        try:
            @zk_client.DataWatch(Env.task_topic)
            def watch_task(data, stat):
                try:
                    msg_value = eval(data.decode())
                    if (type(msg_value) is dict) and (msg_value.get('msgType') == 'taskMsg') and (
                        Env.IP in msg_value.get('scanNodes')):
                        self.__scheduler(msg_value)
                    else:
                        return
                except:
                    return
            while True:
                time.sleep(1800)
        except Exception as ex:
            g_logger.error(ex)



if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args)>1:
        try:
            Env.DockerNum=int(args[1])
        except:
            pass
    global zk_client
    try:
        zk_client = KazooClient(hosts=Env.ZookeeperHost)
        zk_client.start()
    except:
        print('can`t connect to zookeeper %s, try again'%Env.ZookeeperHost)
        sys.exit(0)
    taskMgte = TaskMgt()
    Monitor(taskMgte).monitor()
