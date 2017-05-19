from pykafka import KafkaClient
from pykafka.common import OffsetType
client = KafkaClient(hosts="45.76.24.153:9092")
print(client.topics['test'.encode()])
topic = client.topics[b'test']
consumer = topic.get_simple_consumer(consumer_group=b'testgroup',
                reset_offset_on_start=True,
                auto_offset_reset=OffsetType.LATEST)
for message in consumer:
    if message is not None:
        print(message.offset, eval(message.value))
    else:
        print('i am down')