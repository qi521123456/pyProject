import logging, os
from enum import Enum
import psutil
import time
import socket

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
    task_dir = '/home/qiqi/scantest/'  # 末尾一定要有 '/'
    log_name = '/home/qiqi/mylog/log.log'
    # script_home = "/home/Script/"
class Task:
    def __init__(self,task_id, task_strategy, port, ip_src, script_data=None, scan_pro='-sS'):
        self.task_id = task_id
        self.task_strategy = task_strategy
        self.port = port
        self.task_ips = ip_src
        self.task_script = script_data
        self.scan_pro = scan_pro  # TCP or UDP
        self.task_status = TaskStatus.INIT
        self.task_process = None
class TaskResult:
    def __init__(self,taskID,taskStatus,taskResult):
        self.task_id = str(taskID)
        self.task_status = str(taskStatus)
        self.task_result = str(taskResult)
        self.nodeIP =self.get_ip()
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('1.255.255.255', 0))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    def __str__(self):
        return "{'taskID':"+self.task_id+",'taskStatus':"+self.task_status+"," \
                    "'taskResult':"+self.task_result+",'scanNode':"+self.nodeIP+"}"

class NodeStatus:
    def __init__(self):
        time.sleep(0.5)
        self.nodeIP = self.get_ip()
        self.nodeDetail = {
            'cpu': str(psutil.cpu_percent())+'%',
            'tStorage': str(psutil.disk_usage("/").total/(1024*1024)) + 'M',
            'uStorage': str(psutil.disk_usage("/").used/(1024*1024)) + 'M'
        }
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('1.255.255.255', 0))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
    def __str__(self):
        return "{'nodeIP':"+self.nodeIP+",'nodeDetail':"+str(self.nodeDetail)+"}"
class TaskStatus(Enum):
    INIT = "init"
    RUNNING = "running"
    DONE = "done"

class Strategy(Enum):
    PORT = 'port_scan'
    PROTOCOL = 'protocol_sniffer'

class ScanType(Enum):  # 都ip
    IP = "ip_scan"
    AREA = "area_scan"

