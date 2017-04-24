from kazoo.client import KazooClient,KazooState,KeeperState
import logging
import sys,time,threading

logging.basicConfig()

zk = KazooClient(hosts='192.168.202.129:2181',read_only=True)
zk.start()
zk.set("/my/favorite/node3","wo shi 222".encode(),version=1)