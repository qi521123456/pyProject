from kazoo.client import KazooClient
from kazoo.client import KazooState
import threading
import time
zk = KazooClient('192.168.205.27:2181')
zk.start()
flag = True
def listen():
    @zk.add_listener
    def listener(stat):
        if stat == KazooState.CONNECTED:
            print("conn")
        elif stat == KazooState.LOST:
            print("aaa")
        print(stat)


    #zk.add_listener(list#ener)#

    while flag:
        time.sleep(1)

t1 = threading.Thread(target=listen)

t1.start()
time.sleep(2)
#flag = False
t1.join()