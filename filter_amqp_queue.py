import multiprocessing

class c_filter_amqp_queue (object):
   	filter_amqp_queue = None
	_lock = None

	def __init__ (self):
        	global filter_amqp_queue
		global _lock
        	filter_amqp_queue = multiprocessing.Queue() 
		_lock = multiprocessing.Lock()

	def put (self, data):
		'''host_stats_queue.put(data, block=True, timeout=None)'''
		filter_amqp_queue.put(data)

	'''returns a Dictionary {}'''
	def get (self):
		if self.is_empty() is True:
			return False
		else:
			return filter_amqp_queue.get()

	def get_nowait (self):
		return filter_amqp_queue.get_nowait()

	def get_lock (self):
		_lock.acquire()
	
	def release_lock (self):
		_lock.release()

	def close_queue (self):
		host_stats_queue.close()

	def is_empty (self):
		if filter_amqp_queue.empty():
			return True
		else:
			return False

