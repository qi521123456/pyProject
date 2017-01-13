from pykafka import KafkaClient
client = KafkaClient()
print(client.topics['test'.encode()])
topic = client.topics[b'test']
consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print(message.offset, message.value.decode())
    else:
        print('i am down')