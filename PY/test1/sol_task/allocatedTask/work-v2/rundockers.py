import os,sys

PATH = "/opt/scan/"
dockername = "znscan"
def getipaddr(iname="enp4s0f0", mname="docker0"):
    info = os.popen("ifconfig").read()
    il = info.strip().split("\n")
    ip = ""
    mac = ""
    for x,i in enumerate(il):
        if i[:len(iname)]==mname:
            ms = il[x+3]
            mac = ms.strip().split(" ")[1]
        elif i[:len(mname)] == iname:
            ip = il[x+1].strip().split(" ")[1]
    if ip=="" or mac=="":
        print "ip or mac is null"
        sys.exit(0)
    return ip,mac
def makedenv(pyname,path=PATH):
    cmdl = []
    cpl = []
    curdir = sys.path[0]+"/"
    cpl.append("cp %s %s" % (curdir + "scp.py", path))
    for i in range(1,5):
        docker = str(i)
        recv = docker+"/task/recv"
        cmdl.append(path+recv)
        cpl.append("touch %slogs/%s.log"%(path,docker))
        cpl.append("cp -f %s %s"%(curdir+pyname+"dn.py",docker))
    cpl.append("touch %slogs/scp.log" % path)
    cmdl.append(path+"result/z")
    cmdl.append(path + "result/n")
    cmdl.append(path+"logs")
    for i in cmdl:
        if os.path.exists(i):
            continue
        os.system("mkdir -p "+i)
    for i in cpl:
        os.system(i)

def rundocker(pyname="z"):
    try:
        makedenv(pyname)
    except:
        print "wrong makeenv"
        sys.exit(0)
    ip,mac = getipaddr()
    os.system("nohup python "+PATH+"scp.py > /dev/null 2>&1 &")
    for i in range(1,5):
        docker = str(i)+"/"
        rc = 'nohup docker run --env hostip="'+ip+'" --env mac="'+mac+'" -v '+PATH+':'+PATH+' '+dockername+' python3 '+PATH+docker+pyname+'dn.py > /dev/null 2>&1 &'
        os.popen(rc)
        print rc

if __name__ == '__main__':
    rundocker(sys.argv[1])

