import multiprocessing
import serial
import Queue
from sysconfigx import *
from ser_filter_queue import *
from syslog_remote import *

class Serial_Functions():

	def __init__(self):
		global filter_queue
		filter_queue = c_ser_filter_queue()
		self.parse = Parser_Functions()
		self.parse.pareser_init()
		self.parse.ConfigSectionMap()
		self.logger_obj = logger()
		self.logger_obj.remote_host()
		#self.line = "01110742zabeelbashir09"
		self.line = None
		self.lqi = '000'

	def serial_init(self):
		device = self.parse.sys_params['device']
		baudrate = int(self.parse.sys_params['baudrate'])
		timeout_sec = int(self.parse.sys_params['timeout'])
		self.ser = serial.Serial(port = device, baudrate = baudrate, timeout=timeout_sec)
		self.ser.flush()

	def serial_receiver(self):
		print "###Reading SERIAL PORT!!!###"
                self.line = self.ser.readline().strip('\r')
                self.line = self.line.strip('\n')
		self.line = self.line.strip('\x00')
		print self.line
		if '+' in self.line:
			if 'DATA' in self.line:
				self.logger_obj.log ("Info at Serial: " + self.line.strip('\n\r'))
				self.lqi = self.parsed(self.line)
				print 'rejected'
		elif self.line == '\n':
			print 'rejected'
		else:
			if self.line:
				self.logger_obj.log ("Data at Serial: " + self.line.strip('\n\r'))
				filter_queue.put(self.line.strip('\n\r') + self.lqi)
				self.ser.flush()
			else:
				print "no data in serial"
				self.line = None
	def parsed(self, line):
		b = (self.line.index('(') + 1)
		return self.line[b:b+3]
