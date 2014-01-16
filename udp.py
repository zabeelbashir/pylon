import multiprocessing
import serial
import Queue
from sysconfigx import *
from ser_filter_queue import *
from syslog_remote import *

class UDP_Functions():

	def __init__(self):
		global filter_queue
		filter_queue = c_ser_filter_queue()
		self.parse = Parser_Functions()
		self.parse.pareser_init()
		self.parse.ConfigSectionMap()
		self.logger_obj = logger()
		self.logger_obj.remote_host()
		self.line = None

	def udp_init(self):
		self.ip = self.parse.sys_params['ser_ip']
		self.port = int(self.parse.sys_params['ser_port'])
		#try :
		self.udp_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Socket created'
		self.udp_obj.bind((self.ip, self.port))
		self.udp_obj.settimeout(0.001)
#		except socket.error , msg:
#			print 'Socket bind incomplete'

	def udp_receiver(self):
		print "###Reading UDP!!!###"
		try:
			self.line = self.udp_obj.recv(1024).strip('\r\n')
			print self.line
			if self.line:
				self.logger_obj.log ("Data at UDP: " + self.line.strip('\r\n'))
				filter_queue.put(self.line)
			else:
				print "no data in UDP"
		except Exception,e:
			print 'caught a timeout'
		self.line = None

