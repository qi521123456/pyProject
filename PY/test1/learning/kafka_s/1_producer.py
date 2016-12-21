from kafka import KafkaProducer
from kafka.errors import KafkaError
from logging import log
import msgpack, json
producer = KafkaProducer(bootstrap_servers=['10.0.1.188:9092'])

# Asynchronous by default

#for _ in range(10):
producer.send('test', b'+www++')

# # Block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=10)
# except KafkaError:
#     # Decide what to do if produce request failed...
#     log.exception()
#     pass
#
# # Successful result returns assigned partition and offset
# print(record_metadata.topic)
# print(record_metadata.partition)
# print(record_metadata.offset)

# produce keyed messages to enable hashed partitioning
# producer.send('test', key=b'foo', value=b'bar')
#
# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('test', {'key': 'value'})
#
# # produce json messages
# producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
# producer.send('test', {'key': 'value'})
#
# # produce asynchronously
# for _ in range(100):
#     producer.send('test', b'msg')
#
# # block until all async messages are sent
# producer.flush()

# configure multiple retries
# producer = KafkaProducer(retries=5)