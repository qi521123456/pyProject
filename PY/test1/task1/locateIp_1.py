# coding utf-8
import pymongo
import socket
import struct
def get_collection(_host,_db,_coll):
    """链接collection"""
    client=pymongo.MongoClient(host=_host)
    coll=client[_db][_coll]
    return coll
def ip2long(_ip):
    """ip转化为long"""
    packedIP=socket.inet_aton(_ip)
    return struct.unpack('!L',packedIP)[0]
def get_location_byIP(_ip):
    """ip确定位置"""
    coll=get_collection('127.0.0.1','SOL','ipChina')
    ipNum=ip2long(_ip)
    locs = coll.find({"end_ip": {"$gte": ipNum}, "start_ip": {"$lte": ipNum}}, {"_id": 0, "location": 1})
    if locs.count() != 0:
        for item in locs:
            location=item['location']
    else:
        location="unkonwn"
    return "该ip位于："+location


