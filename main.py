import signal
import pika
import threading
from ser import *
from filter_ser import *
from amqp_client import *
from sysconfigx import *
from udp import *
from time import *
from syslog_remote import *

class sysinit():
	def __init__(self):
		pass

	def run(self):
		sys_obj = Parser_Functions()
		sys_obj.pareser_init()
		sys_obj.ConfigSectionMap()

class serial_action(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		a = Serial_Functions()
		a.serial_init()
		while True:
			sleep(0.01)
			filter_queue.get_lock()
			a.serial_receiver()
			filter_queue.release_lock()

class udp_action(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		b = UDP_Functions()
		b.udp_init()
		while True:
			sleep(0.01)
			filter_queue.get_lock()
			b.udp_receiver()
			filter_queue.release_lock()

class filter_action(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		c = Filter_Functions()
		while True:
			sleep(0.01)
			#filter_queue.get_lock()
			c.filter_get_data()
			#filter_queue.release_lock()
			c.filter_action()
			amqp_queue.get_lock()
			c.filter_put_data()
			amqp_queue.release_lock()

class amqp_action(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		d = AMQP_Functions()
		while True:
			sleep(0.01)
			#amqp_queue.get_lock()
			d.get_data()
			d.send_data()
			#amqp_queue.release_lock()

def main():
	logger_obj = logger()
	logger_obj.remote_host()
	logger_obj.log ("System Initialized")

	sysinit_obj = sysinit()
	sysinit_obj.run()

	global filter_queue
	filter_queue = c_ser_filter_queue()

	global amqp_queue
	amqp_queue = c_filter_amqp_queue()


	t0 = serial_action()
	t0.start()

	t1 = udp_action()
	t1.start()

	t2 = filter_action()
	t2.start()

	t3 = amqp_action()
	t3.start()


if __name__ == '__main__':
        main()


