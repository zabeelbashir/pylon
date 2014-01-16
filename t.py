import serial
from random import randint
from time import *

class Serial_Dummy():

	def __init__(self):
		self.device = "/dev/pts/5"
		self.baudrate = 115200
		self.timeout_sec = 10
		self.file_name = "/home/zabeel/Desktop/code/ser_data"
		self.line = None

	def serial_init(self):
		self.ser = serial.Serial(self.device, self.baudrate, timeout=self.timeout_sec)

	def read_file(self):
		self.file = open(self.file_name)
		for self.line in self.file:
			print self.line
			self.serial_writer(self.line)
			sleep(randint(0,3))

	def serial_writer(self, line):
		print "###Writing SERIAL PORT!!!###"
		self.ser.write(self.line) 

if __name__ == '__main__':
	a = Serial_Dummy()
	a.serial_init()
	while(1):
		a.read_file()
