import threading
import time,os
import subprocess
from multiprocessing import Process
def t1():
    print('2',threading.current_thread().name)
    time.sleep(2)
    while True:
        #time.sleep(3)
        print("222")
        time.sleep(2)


def t2():
    #cmd = "ping -n 6 baidu.com"
    #time.sleep(5)
    #while True:
    cmd = ["nmap", "111.111.111.111/24"]
    # print(os.popen(cmd).read())
    subprocess.Popen(cmd).communicate()



print(threading.current_thread().name)
a = threading.Thread(target=t2,name="child") # target=<name> 没有（）
#a = Process(target=t1)
a.start()
print("====")