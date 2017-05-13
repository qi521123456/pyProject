from pykafka import KafkaClient
import time,zipfile

client = KafkaClient()
print(client.topics['test'.encode()])
topic = client.topics[b'test']

ns = {'msg_type':'node_status', 'nodeIP':'192.1.1.1', 'nodeDetail':{'a':92,'b':1}}


with open('D:/test.zip','rb') as zfile:
    result = zfile.read()

res = {'msg_type':'task_result','taskID':'233','taskStatus':'DONE','taskResult':result,'scanNode':'188.2.2.3'}
with topic.get_producer() as producer:
    # for i in range(10):
    #     #producer.produce(('-----test message ' + str(i ** 2)).encode())
    #     time.sleep(2)
    #     producer.produce(str(ns).encode())
    producer.produce(str(res).encode())