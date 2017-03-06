import pymysql.cursors
import os

def getip(ports):
    for port in ports:
        filename = "D:/ips/"+str(port)+".txt"
        outsql = 'mysql -uroot -p123456 -h 10.0.1.188 sol_daily -e "select ' \
                 'device_ip from fofa where device_port= ''%s''" >> %s' % (port,filename)
        print(outsql)
        os.system(outsql)

l = ['7547','8000','8001','8002','8003','8004','8006','8008','8080','8081','8087','8088',
     '81','82','83','84','88','8888','90','9005','9008','9017','9014','9020']

def scanL(path="D:/ips/"):
    for i in os.listdir(path):
        port = i.split('.')[0]
        cmd = "nmap -Pn --script D:/HTTP.nse -p %s -iL %s -oX %s" % (port,path+i,path+'xml/'+port+'.xml')
        print(cmd)
        os.system(cmd)
print(len(l))


def xmls(path="D:/ips/xml/"):
    for i in os.listdir(path):
        filepath = path+i
        print(filepath)
        ips = check_from_xml(filepath)
        print(len(ips))
        alter_check(ips)
