from enum import Enum
import logging, os
import socket
import psutil
import time

def get_ip():
    try:
        c = os.popen("env|grep hostip")
        s = c.read().split("=")
        ip = s[1].strip()
        mc = os.popen("env|grep mac")
        mac = mc.read().split("=")[1].strip()
    except:
        ip = '127.0.0.1'
        mac = '02:42:f1:ce:03:eb'
    return str(ip)

def docker2ip():
    path = os.path.split(os.path.realpath(__file__))[0]
    docker = path[path.rfind('/')+1:]
    return docker+"@"+get_ip()
class Logging:

    def __init__(self):
        path = Env.log_name
        self.logger = logging.getLogger()
        self.shandler = logging.StreamHandler()
        if not os.path.exists(path):
            file_dir = path[:path.rfind('/')]
            os.makedirs(file_dir)
        self.fhandler = logging.FileHandler(path)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.shandler.setFormatter(self.formatter)
        self.fhandler.setFormatter(self.formatter)
        self.logger.addHandler(self.shandler)
        self.logger.addHandler(self.fhandler)
        return self.logger


class Env:
    zk_topic_task = '/tasks'
    zk_topic_result = '/result'
    zk_topic_node = '/node'

    task_dir = '/opt/netscan/scan_task/'
    scan_script = '/opt/netscan/script/'
    province_src = '/opt/province/'
    log_name = '/opt/netscan/logs/log.log'
    # kafla_hosts = "45.76.24.153:9092"
    zookeeper_hosts = "45.76.24.153:2181"
    # master_ip = '45.76.24.153' # 由于docker内连不到外界，将结果传到共享文件夹，然后由同意scp脚本来传输
    master_target = '/opt/net_scan/scan_result/'


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

class TaskResult:
    def __init__(self,task_strategy,taskID,taskStatus,taskResult):
        self.msg_type = "task_result"
        self.task_strategy = task_strategy
        self.task_id = str(taskID)
        self.task_status = str(taskStatus)
        self.result_name = str(taskResult)
        self.node_ip = docker2ip()

    def __str__(self):
        #return "{'msgType':"+self.msg_type+",'taskID':"+self.task_id+",'taskStatus':"+self.task_status+"," \
         #           "'taskResult':"+self.task_result+",'scanNode':"+self.node_ip+"}"
        return str(self.__dict__)


class NodeStatus:
    def __init__(self):
        time.sleep(0.5)
        self.msg_type = "node_status"
        self.nodeIP = get_ip()
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

