try:
    from queue import Queue
    from enum import Enum
    from kazoo.client import KazooClient
    import subprocess
    import threading
    import os,shutil
    import signal
    import utils
    import time
except ImportError as IE:
    print(IE)
    exit()

g_logger = utils.Logging().get_logger()

class TaskMgt:
    """Class for managing tasks"""
    task_queue = Queue(maxsize=0)
    task_list = list()

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
        if not os.path.exists(utils.Env.task_dir):
            try:
                os.makedirs(utils.Env.task_dir)
            except OSError as ex:
                print(ex)

    def __get_command(self, task_env, task):
        scan_script = utils.Env.scan_script + "scan.py"
        command = ["python3",scan_script]
        task_type = ''
        task_id = str(task.task_id)
        if task.task_strategy == utils.Strategy.PORT.value:
            task_type = utils.Strategy.PORT.value
            command.append(task_type)
            command.append(task_id)
            command.append(task_env)
            command.append(task.scan_port)
        else:
            task_type = utils.Strategy.PROTOCOL.value
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
        if task.task_strategy == utils.Strategy.PORT.value:
            s_target = task_env+task_id+".txt"
            d_target = task_env+task_id+".zip"
            os.system("zip -j %s %s" % (d_target, s_target))
        else:
            d_target = task_env+task_id+".zip"
            os.system("zip -j %s %s" % (d_target, (task_env+"*.xml")))

        scan_result = task_env + task_id + ".zip"
        save_result = utils.Env.master_target+utils.ip2topic("/tasks") + "-" + task_id + ".zip"
        save_host = "root@%s:%s" % (utils.Env.master_ip,save_result)
        # os.popen("cp %s %s" % (scan_result,save_result))
        # os.system("scp %s %s" % (scan_result, save_host))
        scp_process = subprocess.Popen("scp %s %s" % (scan_result, save_host), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scp_process.wait()
        while scp_process.returncode!=0:
            pass
        g_logger.info("scp ok,savehost:",save_host)
        result_name = utils.ip2topic("/tasks") + "-" + task_id + ".zip"
        task_result = utils.TaskResult(task.task_strategy,task_id,utils.TaskStatus.DONE.value, result_name)
        try:
            zk_client = KazooClient(utils.Env.zookeeper_hosts)
            zk_client.start()
            zk_client.set("/result",str(task_result).encode('UTF-8'))
            zk_client.stop()
        except Exception as ex:
            print(ex)


    def consume(self):
        taskmgt = TaskMgt()
        task_dir = utils.Env.task_dir
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
                task_env = utils.Env.task_dir + str(task_id) + '/'
                #if os.path.exists(task_env):
                    #shutil.rmtree(task_env)
                try:
                    if os.path.exists(utils.Env.task_dir):
                        shutil.rmtree(utils.Env.task_dir)
                    os.makedirs(task_env)
                except OSError as ex:
                    print(ex)

                ip_file = task_env + 'white.txt'
                if scan_ip is not None:
                    with open(ip_file, 'w',encoding='UTF-8') as opener:
                        opener.writelines(scan_ip)
                else:
                    scan_nodes = task.scan_nodes
                    province_src = utils.Env.province_src + scan_province + ".txt"
                    scan_targets = self.__get_target(province_src, len(scan_nodes), scan_nodes.index(utils.ip2topic("/tasks")))
                    with open(ip_file,'w',encoding='UTF-8') as opener:
                        for target in scan_targets:
                            opener.write(target)

                if task.task_strategy == utils.Strategy.PROTOCOL.value:
                    for index in range(len(task.protocol)):
                        script_name = task.protocol[index].get('protocolName') + ".nse"
                        with open(task_env+script_name,'w+',encoding='UTF-8') as writer:
                            writer.write(task.scripts[index])
                cmd = self.__get_command(task_env,task)
                child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
                task.task_process = child
                task.task_status = utils.TaskStatus.RUNNING
                task.task_process.communicate()
                task.task_status = utils.TaskStatus.DONE
                task.task_process = None
                self.__collect_results(task_env, task)
                #try:
                    #shutil.rmtree(task_env)
                #except OSError:
                    #print("can't delete dirs: %s" % task_env)
            except Exception as ex:
                g_logger.info(ex)


class NodeMgte:
    def __init__(self):
        zk_client = KazooClient(hosts=utils.Env.zookeeper_hosts)
        self.zk = zk_client

    def node_status(self):
        g_logger.info("NodeMgte: node_status")
        #while True:
        node_status = utils.NodeStatus()
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
                task = utils.Task(message.get('taskId'), message.get('scanStrategy'), message.get('scanIp'), message.get('province'), message.get('scanNodes'), message.get('scanPort'), message.get('protocol'), message.get('script'))
                # print(task)
                self.taskmgt.create_task(task)

            else:
                pass
        except Exception as ex:
            g_logger.info(ex)

    def monitor(self):
        thread_consumer = threading.Thread(target=Consumer().consume)
        thread_producer = threading.Thread(target=NodeMgte().node_status)
        thread_consumer.start()
        zk_hosts = utils.Env.zookeeper_hosts
        try:
            zk_client = KazooClient(hosts=zk_hosts)
            zk_client.start()
            @zk_client.DataWatch("/tasks")
            def watch_task(data, stat):
                msg_value = eval(data.decode())
                if (type(msg_value) is dict) and (msg_value.get('msgType') == 'taskMsg') and (utils.ip2topic("/tasks") in msg_value.get('scanNodes')):
                    self.__scheduler(msg_value)
                else:
                    return
            while True:
                time.sleep(1800)
            zk_client.stop()
        except Exception as ex:
            print(ex)



if __name__ == "__main__":
    print("--------")
    taskMgte = TaskMgt()
    Monitor(taskMgte).monitor()
