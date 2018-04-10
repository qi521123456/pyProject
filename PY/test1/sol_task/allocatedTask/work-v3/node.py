try:
    from queue import Queue
    from enum import Enum
    from kazoo.client import KazooClient
    import subprocess
    import threading
    import os,shutil
    import signal
    import logging,logging.handlers
    import time
    import psutil
except ImportError as IE:
    print(IE)
    exit()
class Utils:
    @classmethod
    def localAddr(cls):  #  TODO
        try:
            c = os.popen("env|grep hostip")
            s = c.read().split("=")
            ip = s[1].strip()
            mc = os.popen("env|grep mac")
            mac = mc.read().split("=")[1].strip()
        except:
            ip = '局域网地址ipv4'
            mac = 'docker0 mac地址'
        return str(ip),str(mac)
    @classmethod
    def localPath(cls):
        path = os.path.split(os.path.realpath(__file__))[0]
        return path
class Env:
    PATH = Utils.localPath()
    IP,Docker0_MAC = Utils.localAddr()
    DockerNum = 5   # 默认最多5个docker同时运行，启动项目时可更改
    local_result_path = PATH+'/result/'
    if not os.path.exists(local_result_path):
        os.makedirs(local_result_path)
    target_result_path = "" #  TODO
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
    def __init__(self,task_id, task_strategy, scan_ip, scan_province, scan_nodes, scan_port, protocol, scripts):
        self.task_id = task_id
        self.task_strategy = task_strategy
        if scan_ip is "":
            scan_ip = None
        self.scan_ip = scan_ip
        self.task_status = TaskStatus.INIT
        self.task_process = None
        self.scan_province = scan_province
        self.scan_nodes = scan_nodes
        self.scan_port = scan_port
        self.protocol = protocol
        self.scripts = scripts
class TaskPkl:
    def __init__(self,taskid,scantype,port,script,pct,white):
        self.taskid = taskid
        self.scantype = scantype
        self.port = port
        self.script = script
        self.pct = pct  # tcp or udp
        self.white = white
class TaskResult:
    def __init__(self,task_strategy,taskID,taskStatus,taskResult):
        self.msg_type = "task_result"
        self.task_strategy = task_strategy
        self.task_id = str(taskID)
        self.task_status = str(taskStatus)
        self.result_name = str(taskResult)
        self.node_ip = Env.IP

    def __str__(self):
        #return "{'msgType':"+self.msg_type+",'taskID':"+self.task_id+",'taskStatus':"+self.task_status+"," \
         #           "'taskResult':"+self.task_result+",'scanNode':"+self.node_ip+"}"
        return str(self.__dict__)
class Docker:
    def __init__(self,name,process):
        self.dockerName = name
        self.work_path = Env.PATH+'/'+name+'/'
        if not os.path.exists(self.work_path):
            os.makedirs(self.work_path)
        self.process = process
class NodeStatus:
    def __init__(self):
        time.sleep(0.5)
        self.msg_type = "node_status"
        self.nodeIP = Env.IP
        self.nodeDetail = {
            'cpu': str(psutil.cpu_percent())+'%',
            'tStorage': str(psutil.disk_usage("/").total/(1024*1024)) + 'M',
            'uStorage': str(psutil.disk_usage("/").used/(1024*1024)) + 'M'
        }

    def __str__(self):
        #return "{'msg_type':'%s','nodeIP':'%s','nodeDetail':%s}" % (self.msg_type,self.nodeIP,str(self.nodeDetail))
        return str(self.__dict__)


class TaskStatus(Enum):
    INIT = "init"
    RUNNING = "running"
    DONE = "done"


class Strategy(Enum):
    PORT = 'port_scan'
    PROTOCOL = 'protocol_sniffer'


class ScanType(Enum):
    IP = "ip_scan"
    AREA = "area_scan"
class TaskMgt:
    """Class for managing tasks"""
    task_queue = Queue(maxsize=0)
    task_list = list()
    docker_list = list()
    def create_task(self, task):
        self.task_queue.put(task, block=True)
        self.task_list.append(task)

    def remove_task(self, task_id):
        task_index = -1
        for index, task in enumerate(self.task_list):
            if task.task_id == task_id:
                task_index = index
                break
        if task_index != -1:
            self.task_list.pop(task_index)
            g_logger.info("Task '%s' was removed" % task_id)
        g_logger.warn("There is no task:'%s'" % task_id)

    def get_tasks(self):
        tasks = [task.task_id for task in self.task_list]
        return tasks

    def task_status(self, task_id):
        for task in self.task_list:
            if task.task_id == task_id:
                return task.task_status.value
        g_logger.warn("Task given task_id:'%s' not in task_list" % task_id)
        return None

    def set_task_status(self, task_id, task_status):
        for task in self.task_list:
            if task.task_id != task_id:
                continue
            task.task_status = task_status
            break

    def kill_running_task(self):
        for task in self.task_list:
            if task.task_process is not None:
                 os.killpg(task.task_process.pid, signal.SIGUSR1)
                 g_logger.info("Task id : '%s' was killed" % task.task_id)
        g_logger.warn("There is no running task")


class Consumer:

    def __init_env(self):
        if not os.path.exists(Env.task_dir):
            try:
                os.makedirs(Env.task_dir)
            except OSError as ex:
                print(ex)

    def __get_command(self, task_env, task):
        scan_script = Env.scan_script + "scan.py"
        command = ["python3",scan_script]
        task_type = ''
        task_id = str(task.task_id)
        if task.task_strategy == Strategy.PORT.value:
            task_type = Strategy.PORT.value
            command.append(task_type)
            command.append(task_id)
            command.append(task_env)
            command.append(task.scan_port)
        else:
            task_type = Strategy.PROTOCOL.value
            command.append(task_type)
            command.append(task_id)
            command.append(task_env)
            command.append(str(task.protocol))
        return command

    def __get_target(self, file_name, factor, seq):
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

    def __collect_results(self, task_env, task):
        task_id = str(task.task_id)
        if task.task_strategy == Strategy.PORT.value:
            s_target = task_env+task_id+".txt"
            d_target = task_env+task_id+".zip"
            os.system("zip -j %s %s" % (d_target, s_target))
        else:
            d_target = task_env+task_id+".zip"
            os.system("zip -j %s %s" % (d_target, (task_env+"*.xml")))

        scan_result = task_env + task_id + ".zip"
        save_result = Env.master_target+ip2topic() + "-" + task_id + ".zip"
        # save_host = "root@%s:%s" % (Env.master_ip,save_result)
        os.system("cp %s %s" % (scan_result,save_result))
        # os.system("scp %s %s" % (scan_result, save_host))
        # scp_process = subprocess.Popen("scp %s %s" % (scan_result, save_host), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # scp_process.wait()
        # while scp_process.returncode!=0:
        #     pass
        g_logger.info("cp ok,save :",save_result)
        result_name = docker2ip() + "-" + task_id + ".zip"
        task_result = TaskResult(task.task_strategy,task_id,TaskStatus.DONE.value, result_name)
        try:
            zk_client = KazooClient(Env.zookeeper_hosts)
            zk_client.start()
            zk_client.set(Env.zk_topic_result,str(task_result).encode('UTF-8'))
            zk_client.stop()
        except Exception as ex:
            print(ex)


    def consume(self):
        taskmgt = TaskMgt()
        task_dir = Env.task_dir
        self.__init_env()

        while True:
            if taskmgt.task_queue.empty() is True:
                time.sleep(5)
                continue
            try:
                task = taskmgt.task_queue.get()
                if not task in taskmgt.task_list:
                    continue
                print(task.__dict__)
                task_id = str(task.task_id)
                scan_ip = task.scan_ip
                scan_province = task.scan_province
                task_env = Env.task_dir + str(task_id) + '/'
                # try:
                #     if os.path.exists(Env.task_dir):
                #         shutil.rmtree(Env.task_dir)
                #     os.makedirs(task_env)
                # except OSError as ex:
                #     print(ex)

                ip_file = task_env + 'white.txt'
                if scan_ip is not None:
                    with open(ip_file, 'w',encoding='UTF-8') as opener:
                        opener.writelines(scan_ip)
                else:
                    scan_nodes = task.scan_nodes
                    province_src = Env.province_src + scan_province + ".txt"
                    scan_targets = self.__get_target(province_src, len(scan_nodes), scan_nodes.index(docker2ip()))
                    with open(ip_file,'w',encoding='UTF-8') as opener:
                        for target in scan_targets:
                            opener.write(target)

                if task.task_strategy == Strategy.PROTOCOL.value:
                    for index in range(len(task.protocol)):
                        script_name = task.protocol[index].get('protocolName') + ".nse"
                        with open(task_env+script_name,'w+',encoding='UTF-8') as writer:
                            writer.write(task.scripts[index])
                cmd = self.__get_command(task_env,task)
                child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
                task.task_process = child

                task.task_status = TaskStatus.RUNNING
                task.task_process.communicate()
                task.task_status = TaskStatus.DONE
                task.task_process = None
                self.__collect_results(task_env, task)
                try:
                    shutil.rmtree(task_env)
                except OSError:
                    print("can't delete dirs: %s" % task_env)
            except Exception as ex:
                g_logger.info(ex)


class NodeMgte:
    def __init__(self):
        zk_client = KazooClient(hosts=Env.zookeeper_hosts)
        self.zk = zk_client

    def node_status(self):
        g_logger.info("NodeMgte: node_status")
        #while True:
        node_status = NodeStatus()
        self.zk.start()
        self.zk.set("/nodeStatus",str(node_status).encode())
        self.zk.stop()


class Monitor:
    def __init__(self,taskmgt):
        self.taskmgt = taskmgt

    def __scheduler(self, message):
        try:
            msg_type = message.get('msgType')
            if msg_type is None:
                return
            if msg_type == 'taskMsg':
                task = Task(message.get('taskId'), message.get('scanStrategy'), message.get('scanIp'), message.get('province'), message.get('scanNodes'), message.get('scanPort'), message.get('protocol'), message.get('script'))
                # print(task)
                self.taskmgt.create_task(task)

            else:
                pass
        except Exception as ex:
            g_logger.info(ex)
    def docker_moniter(self):
        '''
        更新docker——list状态
        :return:
        '''
        while True:
            if len(self.taskmgt.docker_list)>0:
                for run_docker in self.taskmgt.docker_list:
                    run_docker.pull()  # 不能少
                    if run_docker.process.returncode==0:
                        self.taskmgt.docker_list.remove(run_docker)
            time.sleep(1)

    def monitor(self):
        thread_consumer = threading.Thread(target=Consumer().consume)
        thread_docker = threading.Thread(target=self.docker_moniter)
        thread_producer = threading.Thread(target=NodeMgte().node_status)
        thread_consumer.start()
        thread_docker.start()
        zk_hosts = Env.zookeeper_hosts
        try:
            zk_client = KazooClient(hosts=zk_hosts)
            zk_client.start()
            @zk_client.DataWatch("/tasks")
            def watch_task(data, stat):
                msg_value = eval(data.decode())
                if (type(msg_value) is dict) and (msg_value.get('msgType') == 'taskMsg') and (ip2topic("/tasks") in msg_value.get('scanNodes')):
                    self.__scheduler(msg_value)
                else:
                    return
            while True:
                time.sleep(1800)
            zk_client.stop()
        except Exception as ex:
            print(ex)



if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args)>1:
        try:
            Env.DockerNum=int(args[1])
        except:
            pass
    taskMgte = TaskMgt()
    Monitor(taskMgte).monitor()
