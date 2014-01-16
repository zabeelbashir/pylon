#!/usr/bin/env python
import pika
from time import *
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.66.101'))
channel = connection.channel()

channel.queue_declare(queue='megInboundQueue')
i = 0
#while True:
channel.basic_publish(exchange='',routing_key='megInboundQueue',body='1:222:S:0:0')
#i += 1
#sleep(0)
print " [x] Sent 'Hello World!'"
connection.close()
