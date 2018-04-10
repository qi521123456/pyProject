import os,sys
import logging,logging.handlers
import pickle

# nohup docker run --env hostip="192.168.120.6" --env mac="02:42:f1:ce:03:eb" --env docker="docker1" -v /opt/scan/:/opt/scan znscan python3 /opt/scan/scan.py /home/lmqdcs/v2/pkl1.pkl > /dev/null 2>&1 &
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
        path = os.path.split(os.path.realpath(__file__))[0]
        doc = os.popen("env|grep docker")
        docker = doc.read().split("=")[1].strip()
        return path,docker
class Env:
    PATH,Docker = Utils.localPath()
    IP,MAC = Utils.localAddr()
    work_path = PATH+'/'+Docker+'/'
    result_path = PATH+'/result/'
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    LocalIp = Docker+"@"+IP
    log = PATH+'/logs/'+Docker+'.log'
class Logging:
    def __init__(self,path):
        self.logger = logging.getLogger()
        self.shandler = logging.StreamHandler()
        file_dir = path[:path.rfind('/')]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.fhandler = logging.handlers.RotatingFileHandler(path,maxBytes=1024*1024,backupCount=3)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.shandler.setFormatter(self.formatter)
        self.fhandler.setFormatter(self.formatter)
        self.logger.addHandler(self.shandler)
        self.logger.addHandler(self.fhandler)
        return self.logger
logger = Logging(Env.log).get_logger()
class Task:
    def __init__(self,recv_task):
        self.taskid = recv_task.taskid
        self.scantype = recv_task.scantype
        self.port = recv_task.port
        self.script = recv_task.script
        self.pct = recv_task.pct  # tcp or udp
        self.white = recv_task.white
class Consume:
    def __init__(self,task):
        self.task = task
    def __zmap_command(self,port,target_file,zwhite):
        SNMP_CMD = "zmap -M udp -B 1M -p 161 --probe-args=hex:302702010004067075626c6963a01a02026f0c020100020100300e300c06082b060102010101000500 -f saddr"
        BACnet_CMD = "zmap -M udp -B 1M -p 47808 --probe-args=hex:810a001101040005010c0c023FFFFF194b -f saddr"
        MOXA_CMD = "zmap -M udp -B 1M -p 4800 --probe-args=hex:0100000800000000 -f saddr"
        port = str(port)
        if port == "161":
            cmd = SNMP_CMD.split(" ")
        elif port == "47808":
            cmd = BACnet_CMD.split(" ")
        elif port == "4800":
            cmd = MOXA_CMD.split(" ")
        else:
            cmd = ['zmap', '-B', '1M','-G',Env.MAC, '-p', port]
        cmd.append("-o")
        cmd.append(target_file)
        cmd.append("-w")
        cmd.append(zwhite)
        os.system("/sbin/ldconfig")
        return " ".join(cmd)
    def __nmap_command(self, task,nwhite):
        cmd = ['nmap','-Pn','-'+task.pct,'--script',task.script,'-p',str(task.port),'-iL',nwhite,'-oX',Env.work_path+str(task.taskid)+"-"+Env.LocalIp+".xml"]
        return " ".join(cmd)

    def __zmap_zip(self, task,s_target):
        taskid = str(task.taskid)
        logger.info("zmap over id is '%s'" % taskid)
        # s_target = task_env + taskid+"-"+Env.LocalIp+ ".txt"
        d_target = Env.work_path + taskid + "-"+Env.LocalIp+".zip"
        os.system("zip -j %s %s" % (d_target, s_target))
        save_result = Env.result_path + taskid+ "-" + Env.LocalIp + ".zip"
        os.system("cp %s %s" % (d_target, save_result))
        logger.info("cp ok,save: %s" % save_result)
    def __nmap_zip(self,task):
        taskid = str(task.taskid)
        d_target = Env.work_path + taskid +"-"+Env.LocalIp+ ".zip"
        os.system("zip -j %s %s" % (d_target, (Env.work_path + "*.xml")))
        save_result = Env.result_path + taskid + "-" + Env.LocalIp + ".zip"
        os.system("cp %s %s" % (d_target, save_result))
        logger.info("cp ok,save: %s"% save_result)
    def consume(self):
        if self.task.scantype == 'port':
            targetfile = Env.work_path+'zres.txt'
            cmd = self.__zmap_command(self.task.port,targetfile,self.task.white)
            logger.info("%s task running"%self.task.taskid)
            os.system(cmd)
            self.__zmap_zip(self.task,targetfile)
            logger.info("%s task done" % self.task.taskid)
        elif self.task.scantype == 'protocol':
            tmpfile = Env.work_path + 'ztmp.txt'
            zcmd = self.__zmap_command(self.task.port, tmpfile, self.task.white)
            logger.info("%s task zmap running" % self.task.taskid)
            os.system(zcmd)
            ncmd = self.__nmap_command(self.task,tmpfile)
            logger.info("%s task nmap running" % self.task.taskid)
            os.system(ncmd)
            self.__nmap_zip(task)
            logger.info("%s task done" % self.task.taskid)
        else:
            logger.error("wrong scan type")

if __name__ == '__main__':
    args = sys.argv
    fr = open(args[1], 'rb')
    pkl = pickle.load(fr)
    task = Task(pkl)
    fr.close()
    Consume(task).consume()

