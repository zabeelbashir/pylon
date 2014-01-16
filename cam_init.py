import socket
import sys

class camera():

	def __init__(self):
		try:
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except socket.error:
			print 'Failed to create socket'
			sys.exit()

	def convert_two_byte(self, data):
		upper = data >> 8
		lower = data & 0x00ff
		return chr(upper) + chr(lower)

	def convert_one_byte(self, data):
		return chr(data)

	def str_hex(self, data):
		temp = ''
		for i in range (0, len(data)):
			temp += ord(data[i])
			print temp
		return str(temp)

	def caller(self, tom):
		if tom == 0: #status
			return self.convert_two_byte(1) + self.convert_two_byte(1111) + 'V' + self.convert_one_byte(0) + self.convert_one_byte(0) + self.convert_two_byte(25) + self.convert_one_byte(0)

		elif tom == 1: #location
			return self.convert_two_byte(1) + self.convert_two_byte(1111) + 'V' + self.convert_one_byte(1) + self.convert_one_byte(0) + self.convert_two_byte(25) + '3332.8620,07307.0553,435.2'

		elif tom == 3: # battery
			return self.convert_two_byte(1) + self.convert_two_byte(1111) + 'V' + self.convert_one_byte(3) + self.convert_one_byte(0) + self.convert_two_byte(25) + self.convert_one_byte(0)

		elif tom == 17: #alert
			return self.convert_two_byte(1) + self.convert_two_byte(1111) + 'V' + self.convert_one_byte(17) + self.convert_one_byte(0) + self.convert_two_byte(25) + self.convert_one_byte(0)

	def sender(self, message):
		self.soc.sendto(message, (str('192.168.66.10'), int(25000)))

##device_id>net_id>device_type>type_of_message>priority>CRC>PDU

def main():
	a = camera()
	message = a.caller(0)
	a.sender(message)
	print message
	message = a.caller(1)
	a.sender(message)
	print message
	message = a.caller(3)
	a.sender(message)
	print message

if __name__ == '__main__':
        main()
