
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import time
import os

class NmapMgmt:
    NMAP_OPTIONS = \
        [
            '-v', '-sn', '-sZ', '-sY', '-sX', '-sW', '-sV', '-sU', '-sT', '-sS', '-sO', '-sN', '-sM', '-sL',
            '-sI', '-sF', '-sC', '-sA', '-r', '-p', '-oX', '-oS', '-oN', '-oG', '-oA', '-n', '-max-parallelism',
            '-max-hostgroup', '-iR', '-iL', '-h', '-g', '-f', '-e', '-d', '-b', '-V', '-T', '-S', '-R', '-Pn',
            '-PY', '-PU', '-PS', '-PP', '-PO', '-PM', '-PE', '-PA', '-O', '-F', '-D', '-A', '-6', '--webxml ',
            '--version-trace', '--version-light', '--version-intensity', '--version-all', '--unprivileged',
            '--ttl', '--traceroute', '--top-ports', '--system-dns', '--stylesheet', '--spoof-mac',
            '--source-port', '--send-ip', '--send-eth', '--script-updatedb', '--script-trace', '--script-help',
            '--script-args-file', '--script-args', '--script', '--scanflags', '--scan-delay', '--resume',
            '--reason', '--privileged', '--port-ratio', '--packet-trace', '--osscan-limit', '--osscan-guess ',
            '--open', '--no-stylesheet', '--mtu', '--min-rtt-timeout', '--min-rate', '--min-parallelism',
            '--min-hostgroup', '--max-scan-delay', '--max-rtt-timeout/initial-rtt-timeout', '--max-retries',
            '--max-rate', '--log-errors', '--ip-options', '--iflist', '--host-timeout', '--excludefile',
            '--exclude', '--dns-servers', '--datadir', '--data-length', '--badsum', '--append-output'
        ]

    def __init__(self):
        self.status = {0: "DONE", 1: "READY", 2: "RUNNING", 3: "CANCELLED", 4: "FAILED"}
        self.task_ids = {}

    def create(self, targets, options):
        task_id = int(time.time())
        if self.__check_options(options):
            taskID = NmapProcess(self.__pre_targets(targets), options)
        else:
            taskID = None
        self.task_ids[task_id] = taskID
        return task_id
    def __start(self,taskID):
        #taskID = self.task_ids.get(task_id)
        if not taskID is None:
            taskID.run()
            return True
        else:
            return False
    def get_result(self,task_id):
        taskID = self.task_ids.get(task_id)
        if self.__start(taskID):
            scan_res = taskID.stdout
        else:
            scan_res = None
        return scan_res
    def get_status(self,task_id):
        taskID = self.task_ids.get(task_id)
        rc = taskID.state
        state = self.status.get(rc)
        return state
    def stop(self,task_id):
        taskID = self.task_ids.get(task_id)
        taskID.stop()

    def __pre_targets(self,targets):
        ips = list()
        if os.path.exists(targets):
            with open(targets) as f:
                for line in f.readlines():
                    ips.append(line.strip())
            return ips
        else:
            return targets

    def __check_options(self,options):
        options = options.split(" ")
        for option in options:
            if option not in NmapMgmt.NMAP_OPTIONS:
                return False
        return True

if __name__ == '__main__':
    n = NmapMgmt()
    id = n.create('D:/res.txt','-sV')
    print(n.get_status(id),time.ctime())
    print(n.get_result(task_id=id))
    while n.get_status(id) != 'DONE':
        pass
    print(n.get_status(id), time.ctime())
