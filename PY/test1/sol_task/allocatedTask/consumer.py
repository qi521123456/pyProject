import subprocess,threading
import os,time,shutil,sys
from queue import Queue
from enum import Enum

class Utils:
    @classmethod
    def localAddr(cls):
        try:
            c = os.popen("env|grep hostip")
            s = c.read().split("=")
            ip = s[1].strip()
            mc = os.popen("env|grep mac")
            mac = mc.read().split("=")[1].strip()
        except:
            ip = '127.0.0.1'
            mac = '02:42:f1:ce:03:eb'
        return str(ip),str(mac)
    @classmethod
    def localPath(cls):
        s = "/"
        if sys.platform[:3] == "win":
            s = "\\"
        path = sys.path[0]
        docker = path[path.rfind(s)+1:]
        return path+s,docker
class Env:
    PATH,Docker = Utils.localPath()
    locip,MAC = Utils.localAddr()
    TaskDir = PATH+"task/"
    TaskRecvDir = TaskDir+"recv/"
    # MasterIp = "192.168.120.33"
    MasterZmapResDir = '/home/lmqdcs/result/z/'
    MasterNmapResDir = '/home/lmqdcs/result/n/'
    LocalIp = Docker+"@"+locip
class ScanType(Enum):
    PORT = "port"
    PROTOCOL = "protocol"
class TaskStatus(Enum):
    INIT = "init"
    RUNNING = "running"
    DONE = "done"


class Task:
    def __init__(self,taskid,type,port,nmaphosts,scriptname,pct):
        self.taskid = taskid
        self.type = type
        self.port = port
        self.nmaphosts = nmaphosts
        self.scriptname = scriptname
        self.pct = pct  # tcp or udp
        self.process = None
        self.status = TaskStatus.INIT


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
    def isIn(self,task):
        return task in self.tasks

class Consume:
    def __init__(self,taskmgt):
        self.scantype = ScanType
        self.env = Env
        self.taskStatus = TaskStatus
        self.taskmgt = taskmgt
    def __zmap_command(self, task_env, task):
        os.system("/sbin/ldconfig")
        command = ['zmap', '-B', '1M','-G',self.env.MAC, '-p', str(task.port), '-o', task_env+str(task.taskid)+"-"+self.env.LocalIp+".txt", '-w', task_env+"white.txt"]
        return command
    def __nmap_command(self,task_env, task):
        cmd = ['nmap','-Pn',task.pct,'--script',task_env+task.scriptname+".nse",'-p',str(task.port),'-iL',task_env+"white.txt",'-oX',task_env+str(task.taskid)+"-"+self.env.LocalIp+".xml"]
        return cmd

    def __zmap_zip(self,task_env, task):
        task_id = str(task.taskid)
        s_target = task_env + task_id+"-"+self.env.LocalIp+ ".txt"
        d_target = task_env + task_id + "-"+self.env.LocalIp+".zip"
        os.system("zip -j %s %s" % (d_target, s_target))

        scan_result = task_env + task_id + "-" + self.env.LocalIp + ".zip"
        save_result = self.env.MasterZmapResDir + str(task.taskid)+"-"+task.type+"-"+str(task.port)+"-"+str(task.nmaphosts)+"-"+task.scriptname+"-"+task.pct + "-" + self.env.LocalIp + ".zip"
        scp_process = subprocess.Popen("cp %s %s" % (scan_result, save_result), shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        scp_process.wait()
        while scp_process.returncode != 0:
            pass
        # passg_logger.info("scp ok,savehost:",save_host)
        print("cp ok,save:", save_result)
    def __nmap_zip(self,task_env,task):
        task_id = str(task.taskid)
        d_target = task_env + task_id +"-"+self.env.LocalIp+ ".zip"
        os.system("zip -j %s %s" % (d_target, (task_env + "*.xml")))

        scan_result = task_env + task_id + "-" + self.env.LocalIp + ".zip"
        save_result = self.env.MasterNmapResDir + task_id + "-" + self.env.LocalIp + ".zip"
        # save_host = "root@%s:%s" % (self.env.MasterIp, save_result)
        scp_process = subprocess.Popen("cp %s %s" % (scan_result, save_result), shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        scp_process.wait()
        while scp_process.returncode != 0:
            pass
        # passg_logger.info("scp ok,savehost:",save_host)
        print("cp ok,save:", save_result)

    def consume(self):
        tasks = self.taskmgt
        while True:
            if tasks.isEmpty():
                time.sleep(5)
                continue
            task = tasks.popTask()
            task_env = self.env.TaskDir+task.taskid+"/"
            cmd = self.__zmap_command(task_env, task)
            child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
            task.process = child
            task.status = self.taskStatus.RUNNING
            task.process.communicate()
            task.status = self.taskStatus.DONE
            task.process = None
            self.__zmap_zip(task_env, task)
            try:
                shutil.rmtree(task_env)
            except OSError:
                print("can't delete dirs: %s" % task_env)

class Produce:
    def __init__(self, taskmgt):
        self.env = Env
        self.taskmgt = taskmgt

    def produce(self):
        recvDir = self.env.TaskRecvDir
        tasks = self.taskmgt
        thread_consumer = threading.Thread(target=Consume(tasks).consume)
        thread_consumer.start()
        while True:
            files = os.listdir(recvDir)
            if len(files)<1:
                pass
            for filename in files:
                mtime = os.path.getmtime(recvDir + filename)
                ntime = time.time()
                if ntime-mtime > 60:
                    info = filename[:filename.rfind(".zip")].split("-")
                    taskid = info[0]
                    port = info[2]
                    tasktype = info[1]
                    nmapHosts = info[3]
                    scriptname = info[4]
                    pct = info[5]
                    task = Task(taskid,tasktype,port,nmapHosts,scriptname,pct)
                    task_env = self.env.TaskDir+taskid+"/"
                    if os.path.exists(task_env):
                        shutil.rmtree(task_env)
                    os.mkdir(task_env)
                    unzip = "unzip -o "+recvDir+filename+" -d "+task_env
                    print(unzip)
                    os.system(unzip)
                    txt = "white.txt"
                    for i in os.listdir(task_env):
                        if i.rfind(".txt") !=-1 and i!=txt:
                            os.rename(task_env+i,task_env+txt)
                    tasks.addTask(task)

                    os.remove(recvDir+filename)





if __name__ == '__main__':
    # taskmgt = TaskMgt()
    # Produce(taskmgt).produce()
    txt = "white.txt"
    task_env = "E:/1/"
    for i in os.listdir(task_env):
        if i.rfind(".txt") != -1 and i != txt:
            os.rename(task_env + i, task_env + txt)