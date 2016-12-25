from kafka import KafkaConsumer
import json,msgpack
# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('test',bootstrap_servers=['localhost:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          str(message.value,'utf-8')))
    try:
        d = eval(message.value.decode("utf-8"))
        print(d.get("task_id"))
    except:
        pass

# # consume earliest available messages, don't commit offsets
# KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)
