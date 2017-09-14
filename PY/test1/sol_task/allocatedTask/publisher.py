import os,time,zipfile
import threading
from queue import Queue

class Utils:
    @classmethod
    def spp(cls,hosts, file, path):
        nh = len(hosts)
        l = []
        n = nh
        with open(file, 'r') as fr:
            lines = fr.readlines()
            nl = len(lines)
            if nh > nl:
                n = nl
            for i in range(n):
                l.append([])
            for i, line in enumerate(lines):
                for j in range(n):
                    if i % n == j:
                        l[j].append(line)
        hs = hosts[:n]
        for i, il in enumerate(l):
            write_file = path + hs[i] + ".txt"
            with open(write_file, 'w', encoding="utf8") as fw:
                fw.writelines(il)
        return n
class Env:
    Config = "/root/data/config/config"
    ConfigSeconds = 5
    ScriptsDir = "/root/data/scripts"
    TaskDir = "/root/data/task/z/"
    ZmapTaskPath = "/root/data/"

    NmapTaskPath = "/root/data/"
    TmpDir = "/root/data/tmp/"
    TmpSeconds = 60
    TmpTaskDir = "/root/data/task/tmp/"
    ResultDir = "/root/data/result/"
    ZmapResBackupDir = "/root/data/backup/portscan/"
    NmapResBackupDir = "/root/data/backup/protocolscan/"
    def __str__(self):
        return [self.Config,self.ScriptsDir,self.TaskDir,self.ZmapTaskPath,self.NmapTaskPath,self.TmpDir,self.TmpTaskDir,self.ResultDir,self.ZmapResBackupDir,self.NmapResBackupDir]

class zTask:
    def __init__(self,taskid,type,port,zmaphosts,nmaphosts,scriptname,pct,ips,ipfile):
        self.taskid = taskid
        self.type = type
        self.port = port
        self.ips = ips
        self.ipfile = ipfile
        self.zmaphosts = zmaphosts
        self.nmaphosts = nmaphosts
        self.scriptname = scriptname
        self.pct = pct  # tcp or udp
class nTask:
    def __init__(self,taskid,type,port,nmaphosts,scriptname,pct,ihost):
        self.taskid = taskid
        self.type = type
        self.port = port
        self.nmaphosts = nmaphosts
        self.scriptname = scriptname
        self.pct = pct  # tcp or udp
        self.ihost = ihost
    def __str__(self):
        return str(self.taskid)+"-"+self.type+"-"+str(self.port)+"-"+str(self.nmaphosts)+"-"+self.scriptname+"-"+self.pct
class TaskMgt:
    task_queue = Queue(maxsize=0)
    tasks = []
    def addTask(self,task):
        self.task_queue.put(task)
        self.tasks.append(task)
    def isEmpty(self):
        return self.task_queue.empty()
    def popTask(self):
        task = self.task_queue.get()
        self.tasks.remove(task)
        return task
    def isIn(self,taskid):
        for t in self.tasks:
            if str(taskid) == str(t.taskid):
                return True
        return False

class zPublish:
    configfile = Env.Config	
    tasks = TaskMgt()
    def getConfig(self):
        thread_consumer = threading.Thread(target=self.p2zmap)
        thread_consumer.start()
        s = Env.ConfigSeconds
        while True:
            mtime = os.path.getmtime(self.configfile)
            ntime = time.time()
            if ntime-mtime<=s:
                with open(self.configfile, "r") as fr:
                    lines = fr.readlines()
                    for line in lines:
                        d = eval(line.strip())
                        tid = str(d.get("id"))
                        ips = d.get("ips")
                        ipfile = d.get("ipfile")
                        tasktype = d.get("type")
                        port = str(d.get("port"))
                        zmapHosts = eval(d.get("zmaphosts"))
                        nmapHosts = eval(d.get("nmaphosts"))
                        scriptname = d.get("scriptname")
                        pct = d.get("pct")
                        task = zTask(tid,tasktype,port,zmapHosts,nmapHosts,scriptname,pct,ips,ipfile)
                        self.tasks.addTask(task)

            time.sleep(s)
            continue
    def p2zmap(self):
        taskdir = Env.TaskDir
        zmappath = Env.ZmapTaskPath
        ztdir = "/task/"
        while True:
            if self.tasks.isEmpty():
                time.sleep(Env.ConfigSeconds)
                continue
            task = self.tasks.popTask()
            taskid = task.taskid
            tasktype = task.type
            port = task.port
            zmapHosts = task.zmaphosts
            nmapHosts = task.nmaphosts
            scriptname = task.scriptname
            pct = task.pct
            ips = task.ips
            ipfile = task.ipfile
            zipname = taskid + "-" + tasktype + "-" + port + "-" + str(nmapHosts) + "-" + scriptname +"-"+pct+ ".zip"
            zippath = taskdir + zipname
            if ips != "" and type(eval(ips)) is list:
                ipfile = taskdir + "white.txt"
                with open(ipfile, 'w', encoding="utf8") as fw:
                    for ip in eval(ips):
                        fw.write(ip + "\n")
            n = Utils.spp(zmapHosts,ipfile,taskdir)
            for zhost in zmapHosts[:n]:
                with zipfile.ZipFile(zippath, 'w', compression=zipfile.ZIP_DEFLATED) as zfw:
                    zfw.write(taskdir+zhost+".txt", "white.txt")
                os.system("rm -f %s"% taskdir+zhost+".txt")
                dh = zhost.split("@")
                docker = dh[0]
                hostip = dh[1]
                target = zmappath + docker + ztdir + zipname
                shost = "root@%s:%s" % (hostip, target)
                scp = "scp %s %s" % (zippath, shost)
                os.system(scp)
                os.system("rm -f %s"% zippath)

class nPublish:
    tasks = TaskMgt()
    def getTmp(self):
        thread_consumer = threading.Thread(target=self.t2nmap)
        thread_consumer.start()
        s = Env.TmpSeconds
        tmpdir = Env.TmpDir
        ttdir = Env.TmpTaskDir
        zrbd = Env.ZmapResBackupDir
        # nrbd = Env.NmapResBackupDir
        while True:
            for filename in os.listdir(tmpdir):
                f = os.path.join(tmpdir,filename)
                mtime = os.path.getmtime(f)
                ntime = time.time()
                if ntime-mtime>=s:
                    fns = filename[:filename.rfind(".zip")]
                    info = fns.split("-")
                    if len(info)==2:
                        zmv = "mv %s %s"%(f,zrbd)
                        os.system(zmv)
                    else:
                        taskid = info[0]
                        port = info[2]
                        tasktype = info[1]
                        nmapHosts = eval(info[3])
                        scriptname = info[4]
                        pct = info[5]
                        ihost = info[6]
                        task = nTask(taskid,tasktype,port,nmapHosts,scriptname,pct,ihost)
                        uzip = "unzip -o %s -d %s"%(f,ttdir)
                        os.system(uzip)
                        os.system("rm -f %s"% f)
                        os.rename(ttdir + "white.txt", fns+".txt")

                        self.tasks.addTask(task)
                continue
            time.sleep(s)
            continue
    def t2nmap(self):
        ttdir = Env.TmpTaskDir
        scriptdir = Env.ScriptsDir
        s = Env.TmpSeconds
        nmaptaskpath = Env.NmapTaskPath
        ntdir = "/task/"
        while True:
            if self.tasks.isEmpty():
                time.sleep(s)
                continue
            task = self.tasks.popTask()
            taskid = task.taskid
            tasktype = task.type
            port = task.port
            nmapHosts = task.nmaphosts
            scriptname = task.scriptname
            pct = task.pct
            ihost = task.ihost
            whitetxt = ttdir+task+"-"+ihost+".txt"
            n = Utils.spp(nmapHosts, whitetxt, ttdir)
            os.system("rm -f %s" % whitetxt)
            zipname = task+".zip"
            zippath = ttdir+zipname
            for nhost in nmapHosts[:n]:
                os.system("zip %s %s %s"%(zippath,ttdir+nhost+".txt",scriptdir+scriptname+".nse"))
                os.system("rm -f %s"% ttdir+nhost+".txt")
                dh = nhost.split("@")
                docker = dh[0]
                hostip = dh[1]
                target = nmaptaskpath + docker + ntdir + zipname
                shost = "root@%s:%s" % (hostip, target)
                scp = "scp %s %s" % (zippath, shost)
                os.system(scp)
                os.system("rm -f %s"% zippath)






if __name__ == '__main__':
    # z = threading.Thread(target=zPublish().getConfig)
    # n = threading.Thread(target=nPublish().getTmp)
    # z.start()
    # n.start()
    for i in Env().__str__():
        print(i)
