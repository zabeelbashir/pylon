import logging
#import logging.handlers
from logging.handlers import SysLogHandler

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

#handler = logging.handlers.SysLogHandler(address = '/dev/log')
#handler = logging.handlers.SysLogHandler(address = ('localhost',514), facility=LOG_USER)
handler = logging.handlers.SysLogHandler(address = ("192.168.2.105",514))
#handler = logging.handlers.SysLogHandler(address = '/dev/log' , facility=2)

my_logger.addHandler(handler)

my_logger.debug('this is debug')
my_logger.critical('this is critical')
