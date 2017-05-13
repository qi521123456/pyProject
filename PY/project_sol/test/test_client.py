import subprocess
import time
import os, signal


class TaskClient:
    def __init__(self, id, path, strategy, port):
        self.task_id = id
        self.data_path = path
        self.scan_strategy = strategy
        self.port = port

    def creat(self, scan_type=None, script=''):
        cmd = ['python3', 'scan.py', self.scan_strategy, self.task_id, self.data_path, self.port]
        if scan_type is not None:
            cmd.append(scan_type)
            cmd.append(script)
        child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
        self.child = child
        return child

    def get_status(self):
        return self.child.poll()


if __name__ == "__main__":
    path = "/home/qiqi/test1/test4/"
    t = TaskClient('3234', path, 'port_scan', '80')
    chold = t.creat()
    c = 0
    while True:
        print(chold.poll(), c)
        if c == 5:
            os.killpg(chold.pid, signal.SIGUSR1)
            # chold.kill()
            # break

        time.sleep(3)
        c += 1
