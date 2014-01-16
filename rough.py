import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=10)
ser.write('hello\n')
ser.readline()
