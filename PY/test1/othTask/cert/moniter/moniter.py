import os,time
log = "/root/log/ping.log"
def logping(ip):
    cmd="ping -q -c 10 -i 0.5 "+ip
    info = os.popen(cmd).read()
    r = info.split("\n")[3].split(',')[2].strip().split(" ")[0]
    if r!="0%":
        with open(log,'a+') as fw:
            fw.write("[%s] %s 丢包率'%s'\n"%(ip,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),r))


if __name__ == '__main__':
    # for i in range(39,51):
    #     ip = "10.102.120."+str(i)
    #     logping(ip)
    #     time.sleep(60)
    l = ["2011/12/06","27/10/2009","2009-10-28","09/10/27"]
    for i in l:
        try:
            if i.find('-')!=-1:
                d = i.split('-')
            elif i.find('/')!=-1:
                d= i.split('/')
            for j in d:
                k = int(j)
                if len(j)>2 or k>31:
                    y = j
                elif k<12:
                    m = j
                else:
                    dd = j
            date = y+"-"+m+"-"+dd
        except:
            date = None

        print(date)