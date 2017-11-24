import pika
credentials = pika.PlainCredentials('admin','admin123')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.205.27',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue='rabbitMQ.test',auto_delete="false")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='rabbitMQ.test',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
