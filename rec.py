#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.105'))

channel = connection.channel()

channel.queue_declare(queue='megInboundQueue')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

channel.basic_consume(callback,queue='megInboundQueue',no_ack=True)

channel.start_consuming()
