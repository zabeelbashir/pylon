import pika
import multiprocessing
from sysconfigx import *
from filter_amqp_queue import *
from syslog_remote import *

class AMQP_Functions():

	def __init__(self):
		global amqp_queue
		amqp_queue = c_filter_amqp_queue()
		self.flag = 0
		self.parse = Parser_Functions()
		self.parse.pareser_init()
		self.parse.ConfigSectionMap()
		self.logger_obj = logger()
		self.logger_obj.remote_host()
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(self.parse.sys_params['qhost'])))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=str(self.parse.sys_params['queue_name']))
		self.line = ' '

	def send_data(self):
		try:
			if (self.flag == 1):
				self.channel.basic_publish(exchange='', routing_key=str(self.parse.sys_params['routing_key']), body=str(self.line))
				print " [x] Sent 'Hello World!'"
			else:
				print "waiting for data"
		except Exception:
			self.logger_obj.log ("Exception in Data Send Over AMQP; Will be restarted")
			self.connection.close()
			self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(self.parse.sys_params['qhost'])))
			self.channel = self.connection.channel()
			self.channel.queue_declare(queue=str(self.parse.sys_params['queue_name']))

	def close(self):
		self.connection.close()

	def get_data(self):
		if(amqp_queue.is_empty() is True):
			self.flag = 0
		else:
			print "Filter Get Data!!!"
			self.line = amqp_queue.get()
			self.logger_obj.log ("Data Received form AMQP_Queue: " + str(self.line))
			print "received line at amqp_client= " + str(self.line)
			self.flag = 1
