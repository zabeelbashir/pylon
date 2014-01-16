import multiprocessing
import json
from sysconfigx import *
from ser_filter_queue import *
from filter_amqp_queue import *
from syslog_remote import *
import string

class Filter_Functions():

	def __init__(self):
		global filter_queue
		filter_queue = c_ser_filter_queue()
		global amqp_queue
		amqp_queue = c_filter_amqp_queue()
		self.flag = 0
		self.parse = Parser_Functions()
		self.parse.pareser_init()
		self.parse.ConfigSectionMap()
		queue=str(self.parse.sys_params['queue_name'])
		self.logger_obj = logger()
		self.logger_obj.remote_host()
		self.dict = {'NetID' : '' , 'DevID' : '' , 'Dev_Type' : '' , 'Type' : '' , 'Priority' : '' , 'PDU' : '' , 'ERRC' : ''}
		self.json_obj = None

	def filter_get_data(self):
		if(filter_queue.is_empty() is True):
			self.flag = 0
		else:
			print "Filter Get Data!!!"
			self.line = filter_queue.get()
			if self.line is None:
				self.flag = 0
			else:
				self.logger_obj.log ("Data Received form Filter_Queue: " + str(self.line))
				self.flag = 1
	
	def filter_action(self):
#		try:
		if self.flag == 1:
			self.line = map(ord, self.line)
			print self.line
			print "Filter Action!!!"
			self.dict['NetID'] = str(self.concatinate(self.line[0],self.line[1]))
			print self.dict['NetID']
			self.dict['DevID'] = str(self.concatinate(self.line[2],self.line[3]))
			print self.dict['DevID']
			self.dict['Dev_Type'] = int(self.line[4])
			print self.dict['Dev_Type']
			self.dict['Type'] = str(self.line[5])
			print self.dict['Type']
			self.dict['Priority'] = str(self.line[6])
			print self.dict['Priority']
			self.dict['ERRC'] = str(self.concatinate(self.line[7],self.line[8]))
			print self.dict['ERRC']
			self.dict['PDU'] = str(self.hex_str(self.line[9:]))
			print self.dict['PDU']
#				self.dict['PDU'] = str(self.hex_str(self.line[7:-2]))
#				self.dict['ERRC'] = str(self.concatinate(self.line[-2],self.line[-1]))
############################################## CHANGE HERE !!!!! ##############################################
#				self.json_obj = json.dumps([{'NetID' : self.dict['NetID']} , {'DevID': self.dict['DevID']} , {'Dev_Type': self.dict['Dev_Type']} , {'Type': self.dict['Type']} , {'Priority': self.dict['Priority']} , {'PDU': self.dict['PDU']} , {'ERRC': self.dict['ERRC']}])
			self.json_obj = self.dict['NetID'] + ':' + self.dict['DevID'] + ':' + chr(self.dict['Dev_Type']) + ':' + self.dict['Type'] + ':' + self.dict['PDU']
#				self.json_obj = json.JSONEncoder().encode({'NetID' : self.dict['NetID'] , 'DevID': self.dict['DevID'] , 'Dev_Type': self.dict['Dev_Type'] , 'Type': self.dict['Type'] , 'Priority': self.dict['Priority'] , 'PDU': self.dict['PDU'] , 'ERRC': self.dict['ERRC']})

			self.logger_obj.log ("JSON Formated: " + self.json_obj)
		else:
			print "waiting for data in filter action"
#		except Exception:
#			self.flag == 0
#			print "Data Incomplete"

	def hex_str(self, array):
		print "received for string conversion is: " + str(array)
		temp = ''
		if (self.dict['Type'] == '17'):
#			for i in range (0, len(array)):
			temp = str(array[0]) + ',' + str(array[1])
			print temp
			return str(temp)
		if (self.dict['Type'] == '1'):
			for i in range (0, len(array)):
				temp += chr(array[i])
			self.logger_obj.log ("Data Received for Kill Murphy: " + str(temp))
			gps = temp.split(',')
			self.logger_obj.log ("Data Received for Kill Murphy Splited: " + str(gps))
			temp = self.kill_murphy(gps)
			self.logger_obj.log ("Data Received from Kill Murphy in LIST: " + str(temp))
			temp = temp[0] + ',' + temp[1] + ',' + temp[2]
			self.logger_obj.log ("Data Received for Kill Murphy in FORMATTED: " + str(temp))
			return temp
		else:
			if (len(array) == 1):
				return str(array[0])
			else:
				for i in range (0, len(array)):
					temp += chr(array[i])
				print temp
				return str(temp)

	def kill_murphy(self, gps_coords):
		gps_coords[0] = str(self.toDecimalDegrees(gps_coords[0]))
		gps_coords[1] = str(self.toDecimalDegrees(gps_coords[1]))
		return gps_coords

	def toDecimalDegrees(self, ddmm):
		splitat = string.find(ddmm, '.') - 2
		return self._float(ddmm[:splitat]) + self._float(ddmm[splitat:]) / 60.0

	def _float(self, s):
		if s:
			return float(s)
		else:
			return None

	def concatinate(self, data1 , data2):
		temp = data1 << 8
		final = temp | data2
		return final

	def filter_put_data(self):
		if self.flag == 1:
			print "Filter Put Data!!!"
			amqp_queue.put(self.json_obj)
		else:
			print "waiting for data in filter put"
