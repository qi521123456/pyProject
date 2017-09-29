import os,threading

def genkey(ip):
    cmd = '''ssh '''+ip+''' "ssh-keygen -t rsa -P ''"'''
    os.system(cmd)
    key = os.popen("ssh "+ip+" 'cat /root/.ssh/my_rsa.pub'").read()
    return key
def write2auth(ips):
    with open("/root/.ssh/tmpauth.txt",'a+') as fw:
        for ip in ips:
            key = genkey(ip)
            fw.write(key)

def tran2ip(ip):
    cmd = "scp /home/lmq/znz.zip root@"+ip+":/root"
    os.system(cmd)
    os.system("ssh "+ip+" 'unzip /root/znz.zip'")
    os.system("ssh "+ip+" 'rm -f /root/znz.zip'")
    os.system("ssh "+ip+" 'cat /root/znscan.tar | docker import - znscan'")

def getfromip(ip):
    zcmd = "ssh "+ip+" 'zip -r /root/"+ip+".zip /root/data/test*'"
    os.system(zcmd)
    scpcmd = "ssh "+ip+" 'scp /root/"+ip+".zip root@10.102.120.51:/home/lmq'"
    os.system(scpcmd)


def transport(ips):
    for ip in ips:
        a = threading.Thread(target=tran2ip,args=(ip,))
        b = threading.Thread(target=getfromip,args=(ip,))
        a.start()
        b.start()

if __name__ == '__main__':
    ips = ["10.132.181.10","10.132.181.11","10.132.181.12","10.132.181.13","10.132.181.16",
           "10.132.181.18","10.132.181.19","10.132.181.20","10.132.181.21","10.132.181.28",
           "10.132.181.29","10.132.181.3","10.132.181.4","10.132.181.44","10.132.181.7",
           "10.132.181.8","10.132.181.9"]
    write2auth(ips)
    # transport(ips)