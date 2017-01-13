from pykafka import KafkaClient
client = KafkaClient()
print(client.topics['test'.encode()])
topic = client.topics[b'test']
with topic.get_producer() as producer:
    for i in range(4):
        producer.produce(('-----test message ' + str(i ** 2)).encode())