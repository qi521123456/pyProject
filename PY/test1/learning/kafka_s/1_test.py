from kafka import KafkaClient, SimpleProducer, SimpleConsumer
kafka = KafkaClient("localhost:9092")

producer = SimpleProducer(kafka)

print(producer.send_messages("test1","Hello world!"))