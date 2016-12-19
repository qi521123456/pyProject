import logging
from enum import Enum

class Logging:

    def __init__(self):
        self.logger = logging.getLogger()
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        return self.logger

class Env:
    task_dir = '/home/qiqi/scantest/'  # 末尾一定要有 '/'
    # script_home = "/home/Script/"
class Task:
    def __init__(self,task_id, task_strategy, port, ip_src, script_data=None, scan_pro='-sS  '):
        self.task_id = task_id
        self.task_strategy = task_strategy
        self.port = port
        self.task_ips = ip_src
        self.task_script = script_data
        self.scan_pro = scan_pro  # TCP or UDP
        self.task_status = TaskStatus.INIT
        self.task_process = None
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

