from kazoo.client import KazooClient
from kazoo.handlers.gevent import SequentialGeventHandler

zk = KazooClient(hosts="192.168.202.129:2181",handler=SequentialGeventHandler())

# returns immediately
event = zk.start_async()

# Wait for 30 seconds and see if we're connected
event.wait(timeout=3)

if not zk.connected:
    # Not connected, stop trying to connect
    zk.stop()
    raise Exception("Unable to connect.")
import sys

from kazoo.exceptions import ConnectionLossException
from kazoo.exceptions import NoAuthException


def my_callback(async_obj):
    try:
        children = async_obj.get()
        print(children)
    except (ConnectionLossException, NoAuthException):
        sys.exit(1)


# Both these statements return immediately, the second sets a callback
# that will be run when get_children_async has its return value
async_obj = zk.get_children_async("/my/favorite")
#async_obj.rawlink(my_callback)
my_callback(async_obj)