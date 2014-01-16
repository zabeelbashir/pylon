import socket
import sys
import time
import datetime

HOST = '192.168.66.102'   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
 
 
# Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
     
print 'Socket bind complete'

#now keep talking with the client
#while 1:
st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
with open(str(st) + ".txt", "a") as log_file:
	while 1:
		d = s.recvfrom(1024)
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		log_file.write("TIME: " + str(st) + "	ADDRESS: " + str(d[1][0]) + "	MESSAGE: " + d[0])
		print "TIME: " + str(st) + "	ADDRESS: " + str(d[1][0]) + "	MESSAGE: " + d[0]
s.close()
