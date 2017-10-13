import os,time
import threading
import logging
ZresDir = "/opt/scan/result/z/"
NresDir = "/opt/scan/result/n/"
MonitorSeconds = 5
MasterIp = "10.102.120.51"
MasterZmapResDir = '/opt/scantasks/data/tmp/'
MasterNmapResDir = '/opt/scantasks/data/backup/protocolscan/'
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
logger = Logging("/opt/scan/logs/scp.log").get_logger()
def monitordir(src,dst):
    while True:
        files = os.listdir(src)
        if len(files)<1:
            time.sleep(MonitorSeconds)
            continue
        for filename in files:
            if filename.rfind(".zip") == -1:
                continue
            mtime = os.path.getmtime(src)
            ntime = time.time()
            if ntime-mtime>=MonitorSeconds:
                target = "root@%s:%s"%(MasterIp,dst)
                scp_cmd = "scp %s %s"%(src+filename,target)
                os.system(scp_cmd)
                logger.info("scp ok '%s'"%scp_cmd)
                os.system("rm %s"%src+filename)
                logger.info("remove file '%s'" % filename)

if __name__ == '__main__':
    z = threading.Thread(target=monitordir,args=(ZresDir,MasterZmapResDir))
    n = threading.Thread(target=monitordir, args=(NresDir, MasterNmapResDir))
    z.start()
    n.start()


