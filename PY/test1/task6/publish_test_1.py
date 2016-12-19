import redis
r=simpleRedis.S
def get_redis(host='localhost',port=6379,db=0):
    return redis.StrictRedis(host=host,port=port,db=db)
def publish(topic,content):
    print(topic,content)
    get_redis().publish(topic,content)

if __name__ == '__main__':
    for i in range(10):
        publish('qq_test','this is:'+str(i))