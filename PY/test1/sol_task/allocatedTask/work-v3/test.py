import time
dmessage =  {'taskId':'1','scanStrategy':'port_scan','scanIp':'["121.29.29.1/24","121.17.157.4/24"]','province':'','scanNodes':'["192.168.120.6"]','scanPort':'80','protocol':'','script':'','msgType':'taskMsg'}

# from kazoo.client import KazooClient
# zk = KazooClient()
# zk.start()
# mess = zk.get('/taskmgt')
# print(mess)
# mess = eval(mess[0])
# print(mess)
# with open(r"D:\tmp\test.nse",'w',encoding='utf-8') as fw:
#     fw.write(mess.get('script'))
# time.sleep(3)
# zk.close()

print(str("alb\n").strip())
print("-----")