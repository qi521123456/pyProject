from kazoo.client import KazooClient,KazooState
import logging
import sys

logging.basicConfig()

zk = KazooClient(hosts='localhost:2181')
zk.start()

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
@zk.ChildrenWatch("/my/favorite")
def watch_children(children):
    print("Children are now: %s" % children)
@zk.DataWatch("/my/favorite/node1")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
zk.stop()
