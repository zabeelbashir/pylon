import ConfigParser
import socket
import sys

class logger():

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		try:
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except socket.error:
			print 'Failed to create socket'
			sys.exit()
		self.logger_params = {'lhost' : '' , 'lport' : ''}

	def remote_host(self):
		self.conf = ConfigParser.ConfigParser()
		self.conf.read("/home/zabeel/Desktop/MEG/filter_config")
		sections = self.conf.sections()
		options = self.conf.options('LOGGER')
		for option in options:
			try:
				self.logger_params[option] = self.conf.get('LOGGER', option)
				print self.logger_params[option]
			except:
				self.logger_params[option] = None


	def log(self , msg):
		try :
			self.soc.sendto(msg, (str(self.logger_params['lhost']), int(self.logger_params['lport'])))
		except socket.error, msg:
			print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

if __name__ == '__main__':
	a = logger()
	a.log("kjgjhghj")
