from kazoo.client import KazooClient,KazooState,KeeperState
import logging
import sys,time,threading

logging.basicConfig()

zk = KazooClient(hosts='192.168.202.129:2181',read_only=True)
while True:
    zk.start()
    zk.create("/test_ep",None,ephemeral=True)
    #zk.set("/my/favorite","wo shi ai".encode())
    print(zk.get("/test_ep"))
    time.sleep(2)
    zk.stop()
# zk.ensure_path("/my/favorite")
# for i in range(8):
#     zk.create("/my/favorite/node"+str(i), ("a value:%s" % str(i)).encode())
# if zk.exists("/zk_test"):
#     d = zk.get("/my")
#     print(d)
#
#
# else:
#     print(
#     "not exists.")

# children = zk.get_children("/my/favorite", watch=my_func)
# print(children)
#zk.create("/my/favorite/node","how are you ?".encode())
@zk.add_listener
def my_listener(state):
    print(state)
    if state == KazooState.LOST:
        print('lost')
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print('cccc')
    else:
        # Handle being connected/reconnected to Zookeeper
        print('ee')

@zk.ChildrenWatch("/my/favorite")
def watch_children(children):
    print("Children are now: %s" % children)
@zk.DataWatch("/my/favorite/node")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat, data.decode("utf-8")))


# @zk.add_listener
# def watch_for_ro(state):
#     print(state)
#     if state == KazooState.CONNECTED:
#         if zk.client_state == KeeperState.CONNECTED_RO:
#             print("Read only mode!")
#         else:
#             print("Read/Write mode!")
#time.sleep(15)
#zk.stop()
@zk.ChildrenWatch("/my/favorite")
def watch_children(children):
    print("2Children are now: %s" % children)
