import time
dmessage =  {'taskId':'1','scanStrategy':'port_scan','scanIp':'["121.29.29.1/24","121.17.157.4/24"]','province':'','scanNodes':'["192.168.120.6"]','scanPort':'80','protocol':'','script':'','msgType':'taskMsg'}

from kazoo.client import KazooClient
zk = KazooClient('192.168.120.30:2181')
zk.start()
#while 1:
    # mess = eval(mess[0])
  #  if len(mess[0])>0:
   #     print(mess)
   # continue
# with open(r"D:\tmp\test.nse",'w',encoding='utf-8') as fw:
#     fw.write(mess.get('script'))
#time.sleep(3)
#zk.close()

# print(str("alb\n").strip())

@zk.DataWatch("/taskmgt/task")
def watch_task(data, stat):
    try:
        msg_value = eval(data.decode())
        if (type(msg_value) is dict) and (msg_value.get('msgType') == 'taskMsg'):
            print("----2----:",msg_value)
        else:
            return
    except:
        return
while True:
    time.sleep(1800)