# coding=utf-8
import redis
#读写数据库

# r=redis.StrictRedis(host="localhost",port=6379,db=0)
# r.set('foo','bar')
# print(r['foo'])

# -----------------------------------------------------------
# class Database:
#     def __init__(self):
#         self.host = 'localhost'
#         self.port = 6379
#
#     def write(self,website,city,year,month,day,deal_number):
#         try:
#             key = '_'.join([website,city,str(year),str(month),str(day)])
#             val = deal_number
#             r = redis.StrictRedis(host=self.host,port=self.port)
#             r.set(key,val)
#         except Exception as exception:
#             print(exception)
#
#     def read(self,website,city,year,month,day):
#         try:
#             key = '_'.join([website,city,str(year),str(month),str(day)])
#             r = redis.StrictRedis(host=self.host,port=self.port)
#             value = r.get(key)
#             print(value)
#             return value
#         except Exception as exception:
#             print(exception)
#
# if __name__ == '__main__':
#     db = Database()
#     db.write('meituan','beijing',2013,9,1,8000)
#     db.read('meituan','beijing',2013,9,1)
#############################################################################
#批处理
import datetime


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.write_pool = {}

    def add_write(self, website, city, year, month, day, deal_number):
        key = '_'.join([website, city, str(year), str(month), str(day)])
        val = deal_number
        self.write_pool[key] = val

    def batch_write(self):
        try:
            r = redis.StrictRedis(host=self.host, port=self.port)
            r.mset(self.write_pool)
        except Exception as exception:
            print(exception)
    def batch_read(self):
        r = redis.StrictRedis(host=self.host, port=self.port)
        return self.write_pool


def add_data():
    beg = datetime.datetime.now()
    db = Database()
    for i in range(1, 10):
        db.add_write('meituan', 'beijing', 2013, i, 1, i)
    db.batch_write()
    end = datetime.datetime.now()
    print(end - beg)
def read_by_key():
    db = Database()
    for i in range(1, 10):
        db.add_write('meituan', 'beijing', 2222, i, 1, i)
    db.batch_write()
    print(db.batch_read())

if __name__ == '__main__':
    read_by_key()