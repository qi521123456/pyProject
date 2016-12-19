# coding=utf-8
import redis
class SimpleRedis:
    def __init__(self,host='localhost',port=6379):
        self.redis = redis.StrictRedis(host=host,port=port,db=0)
        self.pubsub = self.redis.pubsub()
    def publish(self,topic,content):
        self.redis.publish(topic,content)
    def subscribe(self,topic):
        self.pubsub.subscribe(topic)
    def psubscribe(self,ptopic):
        self.pubsub.psubscribe(ptopic)
    def listen(self):
        for msg in self.pubsub.listen():
            print(msg)