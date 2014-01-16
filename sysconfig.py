import ConfigParser

class Parser_Functions():

	def __init__(self):
		self.sys_params = {'device': '', 'baudrate': '', 'timeout': '', 'devid': '2', 'prio': '1', 'netid': '2', 'tom': '1', 'len': '2', 'hec': '2', 'pdu_min': '0', 'pdu_max': '80','host': '', 'queue_name': ''}


	def pareser_init(self):
		print "Reading Filter Config!!!"
		self.conf = ConfigParser.ConfigParser()
		self.conf.read("/home/zabeel/Desktop/code/filter_config")
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
			return self.sys_params

#if __name__ == '__main__':
 #       a = Parser_Functions()
#	a.pareser_init()
#	print a.ConfigSectionMap()
