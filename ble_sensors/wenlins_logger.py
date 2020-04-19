# @Author: Henri Wenlin
# @Date:   2020-02-27T14:53:02+02:00
# @Email:  henri.wenlin@kone.com
# @Filename: wenlins_logger.py
# @Last modified by:   Henri Wenlin
# @Last modified time: 2020-03-21T16:23:30+02:00

import logging
import sys
import zmq.log.handlers

class loggerClass():
	def __init__(self, name = 'root',logging_level = 'info', file_logging = False, file_logging_level = 'debug', zmq_logging = False, zmq_port = 1003):
		self.name = name
		self.logger = logging.getLogger(name)

		if logging_level.lower() == 'debug':
			logging_level = logging.DEBUG
		elif logging_level.lower() == 'info':
			logging_level = logging.INFO
		elif logging_level.lower() == 'warning':
			logging_level = logging.WARNING
		elif logging_level.lower() == 'error':
			logging_level = logging.ERROR
		elif logging_level.lower() == 'critical':
			logging_level = logging.CRITICAL
		else:
			sys.exit("Error at Wenlin's logger: Used logging level is not supported. Exiting...")

		if file_logging_level.lower() == 'debug':
			file_logging_level = logging.DEBUG
		elif file_logging_level.lower() == 'info':
			file_logging_level = logging.INFO
		elif file_logging_level.lower() == 'warning':
			file_logging_level = logging.WARNING
		elif file_logging_level.lower() == 'error':
			file_logging_level = logging.ERROR
		elif file_logging_level.lower() == 'critical':
			file_logging_level = logging.CRITICAL
		else:
			sys.exit("Error at Wenlin's logger: Used logging level is not supported. Exiting...")

		if name == 'root':
			root = logging.getLogger()
			root.setLevel(logging_level)
		else:
			root = logging.getLogger()
			root.setLevel('DEBUG')			# By this defenition, now all log messages are comming through to console logger. I don't know if this is not pythonic way...

		ch = logging.StreamHandler()
		ch.setLevel(logging_level)
		formatter = logging.Formatter('[{levelname:^17} : {name:^17}]: {message}',style='{')# + '[%(levelname)-7s : %(name)-11s] - %(message)s')
		ch.setFormatter(formatter)
		if not [True for x in self.logger.handlers if x.__class__ == logging.StreamHandler]:
			self.logger.addHandler(ch)
		if file_logging and not [True for x in self.logger.handlers if x.__class__ == logging.FileHandler]:  # Initialize file handler?
			# Create file where logger prints
			fh = logging.FileHandler(name + '.log')
			fh.setLevel(file_logging_level)
			# create formatter and add it to the handlers
			formatter = logging.Formatter(
				'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			fh.setFormatter(formatter)
			# add the handlers to the logge
			self.logger.addHandler(fh)
		if zmq_logging and not [True for x in self.logger.handlers if x.__class__ == zmq.log.handlers.PUBHandlerr]:
			handler = zmq.log.handlers.PUBHandler('tcp://*:' + str(1103))
			handler.root_topic = self.name
			self.logger.addHandler(handler)
		self.logger.setLevel(logging_level)

	def debug(self, msg):
		self.logger.debug(msg)
	def info(self, msg):
		self.logger.info(msg)
	def warning(self, msg):
		self.logger.warning(msg)
	def error(self, msg):
		self.logger.error(msg)
	def critical(self, msg):
		self.logger.critical(msg)
	def exception(self, msg):
		self.logger.exception(msg)


if __name__ == '__main__':
	logger = loggerClass(name = 'Test logger', file_logging = True, logging_level = 'debug', file_logging_level = 'debug')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')

	logger = loggerClass(name = 'Test logger', file_logging = True, logging_level = 'Info', file_logging_level = 'info')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')

	logger = loggerClass(name = 'Test logger', file_logging = True, logging_level = 'Warning', file_logging_level = 'warning')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')

	logger = loggerClass(name = 'Test logger', file_logging = True, logging_level = 'error', file_logging_level = 'error')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')


	logger = loggerClass(name = 'Test logger', file_logging = True, logging_level = 'critical', file_logging_level = 'critical')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')

	logger = loggerClass(name = 'Logging testing', file_logging = True, logging_level = 'debug', file_logging_level = 'debug1')
	debug = logger.debug
	info = logger.info
	warning = logger.warning
	error = logger.error
	critical = logger.critical
	exception = logger.exception
	debug('Debug')
	info('Info')
	warning('Warning')
	error('Error')
	critical('Critical')
	exception('Exception')
