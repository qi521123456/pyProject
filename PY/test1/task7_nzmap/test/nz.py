# coding=utf-8
import os
import time
import re,socket
class CmdMgmt:
    def __init__(self):
        self.task_ids = {}
    def creat(self,cmd='ping 127.0.0.1'):
        tid = time.time()
        cmd = cmd.replace('  ', ' ')
        p = os.popen('nohup '+cmd+' > /dev/null 2>&1 &')
        #p = os.popen(cmd)
        if cmd.find('/'):
            cmd = cmd.replace('/',r'\/')
        q_cmd = r"ps aux | awk '/%s$/{print $2}'" % cmd.strip()
        #print(q_cmd)
        pid = os.popen(q_cmd).readline().strip()
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
            status = True
        else:
            status = False
        return status
    def kill_task(self,tid):
        pid = self.task_ids.get(tid)[0]
        try:
            os.system('kill '+pid)
        except:
            return False
        else:
            return True

    def _ipform(self,ips):
        ip = ips
        if ips.find('/') != -1:
            str1 = ips.split('/')
            if -1<int(str1[1])<33:
                ip = str1[0]
            else:
                print('error targets')
                return False
        str2 = ip.split('.')
        for i in str2:#TODO
            if int(i)<0 or int(i)>255:
                return False
        return True

class ZmapMgmt(CmdMgmt):
    def __init__(self,scan_port=80,scan_ips='127.0.0.1',out_file='res.txt',other_scan_args=''):
        CmdMgmt.__init__(self)
        
        cmd = 'zmap -B 1M -p '+str(scan_port)+' '+other_scan_args+' '
        if os.path.exists(out_file):
            cmd +='-o '+out_file+' '
        if super()._ipform(scan_ips):
            cmd +=scan_ips
        self.tid = super().creat(cmd=cmd)
    def get_result(self,tid):
        super().get_result()
        pass
class NmapMgmt(CmdMgmt):
    def __init__(self):
        CmdMgmt.__init__(self)
    def creat(self,scan_targets='127.0.0.1',outPut_opts=('-oN','res.txt'),other_scan_opts=''):
        cmd = 'nmap '+other_scan_opts+' '
        if os.path.exists(scan_targets):
            cmd +='-iL '+scan_targets+' '
        elif super()._ipform(scan_targets):
            cmd += scan_targets+' '
        else:
            print('error targets')
            return None
        # if outPut_opts[0] in ['-oN', '-oX', '-oS', '-oG', '-oA'] and os.path.exists(outPut_opts[1]):
            # cmd += str(outPut_opts[0])+' '+str(outPut_opts[1])+' '
        tid = super().creat(cmd)
        return tid
class NZAgent:
    def __init__(self,hosts='localhost',port=80,zmap_other_opts='',nmap_other_opts=''):
        path = './tmp/'
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        filename = path+'tmp.txt'
        os.system(r'touch %s' % filename)
        z = ZmapMgmt(port,self.__hostsFormat(hosts),filename,zmap_other_opts)
        print(z.task_ids)
        while z.get_status(z.tid):pass
        n = NmapMgmt()
        n.creat(filename,None,nmap_other_opts)
        print(n.task_ids)



    def __hostsFormat(self,hosts):
        if re.search('/\d{1,2}$',hosts):
            i = hosts.rfind('/')
            left = socket.gethostbyname(hosts[:i])  # url2ip
            hosts = left + hosts[i:]
        else:
            hosts = socket.gethostbyname(hosts)
        return hosts

if __name__ == "__main__":
    # z=ZmapMgmt(80,'','res.txt','-N 1000')
    # print(z.task_ids,z.get_status(z.tid),'===')
    # n = NmapMgmt()
    # id = n.creat('test.txt')
    # print(n.task_ids,'--',n.get_status(id))
    nz = NZAgent('baidu.com/16',80,'','-oN test.txt')
