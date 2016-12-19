import subprocess
import time
class ZmapMgmt:
    def __init__(self):
        self.task_ids = {}
    def execute(self,cmd = r'ping -n 10 baidu.com'):
        id = time.time()
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.task_ids[id] = p
        #p.wait()
        try:
            o, e = p.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            p.kill()
            o, e = p.communicate()
        #yield o.decode('gb2312')

        return id,o.decode('gb2312')
    # def get_result(self,task_id):
    #     p = self.task_ids.get(task_id)
    #
    #     # for line in p.stdout.readlines():
    #     #     yield line.decode('gb2312')
    #        # print(line.decode('gb2312') + r'---\n')
    def kill_task(self,task_id):
        p = self.task_ids.get(task_id)

        if p.poll() is None:
            p.kill()
    def get_status(self,task_id):
        status = self.task_ids[task_id].poll()

        if status is None:
            s = 'ON'
        else:
            s = 'OFF'
        return s,status

if __name__ == '__main__':
    zins = ZmapMgmt()
    id,out = zins.execute()
    print(out)
    zins.kill_task(id)

    # for i in zins.get_result(id):
    #     print(i)
    print(zins.get_status(id))

