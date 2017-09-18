import os,time
import threading

ZresDir = "/home/lmqdcs/result/z/"
NresDir = "/home/lmqdcs/result/n/"
MonitorSeconds = 5
MasterIp = "192.168.120.33"
MasterZmapResDir = '/home/lmq/data/tmp/'
MasterNmapResDir = '/home/lmq/data/backup/protocolscan/'

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
                # os.system(scp_cmd)
                print(scp_cmd)
                os.system("rm %s"%src+filename)

if __name__ == '__main__':
    z = threading.Thread(target=monitordir,args=(ZresDir,MasterZmapResDir))
    n = threading.Thread(target=monitordir, args=(NresDir, MasterNmapResDir))
    z.start()
    n.start()


