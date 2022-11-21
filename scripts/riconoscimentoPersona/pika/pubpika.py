import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='testing')
channel.basic_publish(exchange='',
                      routing_key='testing',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
