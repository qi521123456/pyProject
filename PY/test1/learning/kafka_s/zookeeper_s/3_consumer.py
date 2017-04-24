from kazoo.client import KazooClient,KazooState,KeeperState
import logging
import sys,time,threading

logging.basicConfig()

zk = KazooClient(hosts='192.168.202.129:2181',read_only=True)

while True:
    zk.start()
    # @zk.ChildrenWatch("/my/favorite")
    # def watch_children(children):
    #     print("Children are now: %s" % children)
    print(zk.get("/my/favorite/node3"))
    # @zk.DataWatch("/my")
    # def watch_node(data, stat):
    #     print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    # @zk.add_listener
    # def my_listener(state):
    #     print(state)
    #     if state == KazooState.LOST:
    #         print('lost')
    #         # Register somewhere that the session was lost
    #     elif state == KazooState.SUSPENDED:
    #         # Handle being disconnected from Zookeeper
    #         print('cccc')
    #     else:
    #         # Handle being connected/reconnected to Zookeeper
    #         print('ee')
    zk.stop()
    time.sleep(5)