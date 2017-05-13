import redis
from task6 import simpleRedis
def get_redis(host='localhost',port=6379,db=0):
    return redis.StrictRedis(host=host,port=port,db=db)
def listen_sub(topic):
    r = get_redis()
    p = r.pubsub()
    p.subscribe(topic)
    for msg in p.listen():
        print(msg)

if __name__ == '__main__':
    listen_sub('qq_test')