import os,time
import threading
from queue import Queue
import logging
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
    Config = "/opt/scantasks/data/config/config"
    ConfigSeconds = 5
    ScriptsDir = "/opt/scantasks/data/scripts/"
    TaskDir = "/opt/scantasks/data/task/z/"

    ZmapTaskPath = "/opt/scan/"
    NmapTaskPath = "/opt/scan/"
    EndzntDir = "/task/recv/"

    TmpDir = "/opt/scantasks/data/tmp/"
    TmpSeconds = 60
    TmpTaskDir = "/opt/scantasks/data/task/n/"
    # ResultDir = "/home/lmq/data/result/"
    ZmapResBackupDir = "/opt/scantasks/data/backup/portscan/"
    NmapResBackupDir = "/opt/scantasks/data/backup/protocolscan/"
    def __str__(self):
        return [self.Config,self.ScriptsDir,self.TaskDir,self.ZmapTaskPath,self.NmapTaskPath,self.TmpDir,self.TmpTaskDir,self.ZmapResBackupDir,self.NmapResBackupDir]
class Logging:
    def __init__(self,path):
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
logger = Logging("/opt/scantasks/data/log/scan.log").get_logger()
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
        nhs = "+".join(self.nmaphosts)
        return "-"+self.type+"-"+str(self.port)+"-"+nhs+"-"+self.scriptname+"-"+self.pct
class TaskMgt:
    def __init__(self):
        self.task_queue = Queue(maxsize=0)
        self.tasks = []
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
                        nmapHosts = d.get("nmaphosts")
                        scriptname = d.get("scriptname")
                        pct = d.get("pct")
                        task = zTask(tid,tasktype,port,zmapHosts,nmapHosts,scriptname,pct,ips,ipfile)
                        self.tasks.addTask(task)
                        logger.info("add ztask to queue: %s"%tid)

            time.sleep(s)
            continue
    def p2zmap(self):
        taskdir = Env.TaskDir
        zmappath = Env.ZmapTaskPath
        ztdir = Env.EndzntDir
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
            nps = "+".join(nmapHosts)
            zipname = taskid + "-" + tasktype + "-" + port + "-" + nps + "-" + scriptname +"-"+pct+ ".zip"
            zippath = taskdir + zipname

            if ips != "" and type(eval(ips)) is list:
                ipfile = taskdir + "white.txt"
                with open(ipfile, 'w', encoding="utf8") as fw:
                    for ip in eval(ips):
                        fw.write(ip + "\n")
            n = Utils.spp(zmapHosts,ipfile,taskdir)
            logger.info("get ztask,split ipfile ok,start scp...")
            for zhost in zmapHosts[:n]:
                os.system("zip -j %s %s"%(zippath,taskdir+zhost+".txt"))
                os.system("rm -f %s"% taskdir+zhost+".txt")
                dh = zhost.split("@")
                docker = dh[0]
                hostip = dh[1]
                target = zmappath + docker + ztdir + zipname
                shost = "root@%s:%s" % (hostip, target)
                scp = "scp %s %s" % (zippath, shost)
                os.system(scp)
                os.system("rm -f %s"% zippath)
                logger.info("scp to zmap host '%s' over : '%s'"%(shost,scp))

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
                    if info[1] == "port":
                        zmv = "mv %s %s"%(f,zrbd)
                        os.system(zmv)
                    else:
                        taskid = info[0]
                        port = info[2]
                        tasktype = info[1]
                        try:
                            nmapHosts = eval(info[3])
                        except SyntaxError:
                            nmapHosts = info[3].split("+")
                        scriptname = info[4]
                        pct = info[5]
                        ihost = info[6]
                        task = nTask(taskid,tasktype,port,nmapHosts,scriptname,pct,ihost)
                        uzip = "unzip -o %s -d %s"%(f,ttdir)
                        os.system(uzip)
                        print(uzip)
                        os.system("rm -f %s"% f)
                        self.tasks.addTask(task)
                        logger.info("add ntask to queue: %s" % taskid)
                continue
            time.sleep(s)
            continue
    def t2nmap(self):
        ttdir = Env.TmpTaskDir
        scriptdir = Env.ScriptsDir
        s = Env.TmpSeconds
        nmaptaskpath = Env.NmapTaskPath
        ntdir = Env.EndzntDir
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
            #os.rename(ttdir + str(taskid)+"-"+ihost+".txt", ttdir + str(task)+"-"+ihost + ".txt")
            # whitetxt = ttdir+str(task)+"-"+ihost+".txt"
            whitetxt = ttdir + str(taskid)+"-"+ihost+".txt"
            n = Utils.spp(nmapHosts, whitetxt, ttdir)
            logger.info("get ntask,split ipfile ok,start scp...")
            os.system("rm -f %s" % whitetxt)
            zipname = str(task)+".zip"
            zippath = ttdir+str(taskid)+zipname
            for nhost in nmapHosts[:n]:
                os.system("zip -j %s %s %s"%(zippath,ttdir+nhost+".txt",scriptdir+scriptname+".nse"))
                os.system("rm -f %s"% ttdir+nhost+".txt")
                dh = nhost.split("@")
                docker = dh[0]
                hostip = dh[1]
                target = nmaptaskpath + docker + ntdir + str(taskid)+"+"+str(ihost)+zipname
                shost = "root@%s:%s" % (hostip, target)
                scp = "scp %s %s" % (zippath, shost)
                os.system(scp)
                os.system("rm -f %s"% zippath)
                logger.info("scp to nmap host '%s' over : '%s'" % (shost, scp))






if __name__ == '__main__':
    z = threading.Thread(target=zPublish().getConfig)
    n = threading.Thread(target=nPublish().getTmp)
    z.start()
    n.start()

