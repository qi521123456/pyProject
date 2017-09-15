import os,time

ZresDir = "/home/lmqdcs/result/z/"
NresDir = "/home/lmqdcs/result/n/"
MonitorSeconds = 5
MasterIp = "192.168.120.33"
MasterZmapResDir = '/home/lmq/data/tmp/'
MasterNmapResDir = '/home/lmq/data/backup/protocolscan/'
def scpcmd(zippath):
    scpc = "scp %s %s"%(zippath,)

def monitorZmap(src,dst):
    while True:
        files = os.listdir(src)
        if len(files)<1:
            time.sleep(MonitorSeconds)
            continue
        for filename in files:
            pass