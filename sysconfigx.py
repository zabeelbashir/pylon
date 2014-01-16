import ConfigParser
from syslog_remote import *

class Parser_Functions():

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.sys_params = {'device': '', 'baudrate': '', 'timeout': '', 'devid': '', 'prio': '', 'netid': '', 'tom': '', 'len': '', 'hec': '', 'pdu_min': '', 'pdu_max': '','qhost': '', 'queue_name': '' , 'lhost' : '' , 'lport' : ''}
		self.logger_obj = logger()
		self.logger_obj.remote_host()

	def pareser_init(self):
		print "Reading Filter Config!!!"
		self.conf = ConfigParser.ConfigParser()
		self.conf.read("/home/zabeel/Desktop/MEG/filter_config")
		print self.conf.sections()

	def ConfigSectionMap(self):
		sections = self.conf.sections()
		for section in sections:
			options = self.conf.options(section)
			for option in options:
				try:
					self.sys_params[option] = self.conf.get(section, option)
				except:
					self.sys_params[option] = None
		print self.sys_params
		self.logger_obj.log ("System Initialized with Parameters: " + str(self.sys_params))
		return self.sys_params

if __name__ == '__main__':
	a = Parser_Functions()
	a.pareser_init()
	print a.ConfigSectionMap()
