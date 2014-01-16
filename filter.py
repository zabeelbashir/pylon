import multiprocessing
import ConfigParser
import ser_filter_queue
import filter_amqp_queue

def pareser_init():
	print "Reading Filter Config!!!"
	conf = ConfigParser.ConfigParser()
	conf.read("/home/zabeel/Desktop/code/filter_config")
	print conf.sections()

def filter_init():
	print "Filter Initialized!!!"

def filter_get_data():
	print "Filter Get Data!!!"
	c_ser_filter_queue.get_lock()
	line = c_ser_filter_queue.get()
	c_ser_filter_queue.release_lock()

def filter_action():
	print "Filter Action!!!"

def filter_put_data():
	print "Filter Put Data!!!"
	c_filter_amqp_queue.get_lock()
	c_ser_filter_queue.put(line)
	c_filter_amqp_queue.release_lock()


'''
if __name__ == "__main__":
	pareser_init()
	filter_init()
	filter_get_data()
	filter_action()
	filter_put_data()'''
