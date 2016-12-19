import os
import time
class CmdMgmt:
    def __init__(self):
        self.task_ids = {}
    def creat(self,cmd='ping 127.0.0.1'):
        tid = time.time()
        p = os.popen('nohup '+cmd+' > /dev/null 2>&1 &')
        pid = os.popen("ps aux|awk '/"+cmd+"$/{print $2}'").readline().strip()
        self.task_ids[tid] = (pid,p)
        return tid
    def get_result(self,tid):
        res = self.task_ids.get(tid)[1].read()
        print(res)
    def get_status(self,tid):
        status = None
        pid = self.task_ids.get(tid)[0]
        res = os.popen("ps aux|awk '$2=="+str(pid)+"'").read()
        if res != '':
            status = 'doing'
        else:
            status = 'over'
        return status
    def kill_task(self,tid):
        pid = self.task_ids.get(tid)[0]
        try:
            os.system('kill '+pid)
        except:
            return False
        else:
            return True

class ZmapMgmt(CmdMgmt):
    def __init__(self,scan_port=80,scan_ips='127.0.0.1',out_file='res.txt',other_scan_args=''):
        Cmdmgmt.__init__(self)
        cmd = 'zmap -B 1M -p '+str(scan_port)+' '+other_scan_args+' '
        if os.path.exists(out_file):
            cmd +='-o '+out_file+' '
        cmd +=scan_ips
        self.tid = super().creat(cmd=cmd)
    def get_result(self,tid):
        super().get_result()
        pass



if __name__ == "__main__":
    z=ZmapMgmt(80,'','','-n 1000')
    print(z.task_ids,z.get_status(z.tid),'===')

