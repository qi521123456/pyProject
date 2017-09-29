import os,sys

PATH = "/opt/scan/"
dockername = "znscan"
def getipaddr(iname="wlp8s0", mname="docker0"):
    info = os.popen("ifconfig").read()
    il = info.split("\n")
    for x,i in enumerate(il):
        if i[:len(iname)]==mname:
            ms = il[x+2]
            mac = ms.strip().split(" ")[1]
        elif i[:len(mname)] == iname:
            ip = il[x+1].strip().split(" ")[1]
    return ip,mac
def makedenv(pyname,path=PATH):
    cmdl = []
    cpl = []
    curdir = sys.path[0]
    cpl.append("cp %s %s" % (curdir + "scp.py", path))
    for i in range(1,5):
        docker = "docker"+str(i)
        recv = docker+"/task/recv"
        cmdl.append(path+recv)
        cpl.append("cp -f %s %s"%(curdir+pyname+".py",docker))
    cmdl.append(path+"result/z")
    cmdl.append(path + "result/n")
    for i in cmdl:
        if os.path.exists(i):
            continue
        os.system("mkdir -p "+i)
    for i in cpl:
        os.system(i)

def rundocker(pyname="zdn",macname="enp2s0f0"):
    try:
        makedenv(pyname)
    except:
        #print "wrong makeenv"
        sys.exit(0)
    ip,mac = getipaddr(macname)
    for i in range(1,5):
        docker = "docker"+str(i)
        rc = 'nohup docker run --env hostip="'+ip+'" --env mac="'+mac+'" -v '+PATH+':'+PATH+' '+dockername+' python3 '+PATH+docker+pyname+'.py +> /dev/nill 2>&1 &'
        os.popen(rc)
        #print rc

if __name__ == '__main__':
    a(sys.argv[1])

