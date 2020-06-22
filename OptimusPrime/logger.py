import logging
import logging.handlers
import numpy as np
import os

class MsgRngFilter(logging.Filter):
	# logging filter that requires record to be within specified range of logging levels
	def __init__(self, min_lvl, max_lvl, name=''):
		super().__init__(name=name)
		self.min_lvl = min_lvl
		self.max_lvl = max_lvl

	def filter(self, rec):
		return (self.min_lvl <= rec.levelno <= self.max_lvl)

# new logger level for logging optimus data
DATA_LEVEL = 60
logging.addLevelName(DATA_LEVEL, "DATA")

def data(self, msg, *args, **kwargs):
	if self.isEnabledFor(DATA_LEVEL):
		self._log(DATA_LEVEL, msg, args, **kwargs)

logging.Logger.data = data

class OptimusStreamHandler(Logging.StreamHandler):
	# Custom Stream Handler for Optimus Project
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.addFilter(MsgRngFilter(logging.DEBUG, logging.CRITICAL))

# create logger
logger = logging.getLogger('optimus_logger')
logger.setLevel(logging.DEBUG)
logger.propagate = False   # set to false to that events logged to this logger to not get passed to other handlers

formatter = logging.Formatter('%(message)s')

ch = OptimusStreamHandler()
ch.setLevel(logging.WARNING) #default level of messages warning and up
ch.setFormatter(formatter)

if not os.path.exists('log-reports'):
	os.makedirs('log-reports')

fh=logging.FileHandler('log-reports/optius.log', mode = 'w')
fh.addFilter(msgRngFilter(logging.DEBUG, logging.CRITICAL))
fh.setLevel(logging.INFO)  # default level of messages info and up
fh.setFormatter(formatter)

sh = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
sh.setLevel(DATA_LEVEL)  # level should always be data

logger.addHandler(sh)  #  add at index 0
logger.addHandler(fh)  #  add at index 1
logger.addHandler(ch)  # added at index 2


def remove_stream_handlers():
	# remove from logger created for optimus
	logger.handlers = [h for h in logger.handlers if not (type(h) == logging.StreamHandler)]

	# remove from logging top level logger
	top_logger = logging.getLogger()
	top_logger.handlers = [h for h in top_logger.handlers if not (type(h) == logging.StreamHandler)]


def update_logger_levels_for_verbose():
	logger.handlers[1].setLevel(logging.DEBUG)  # set file handler level to debug and up
	logger.handlers[2].setLevel(logging.DEBUG)  # set stream handler level to debug and up

def fix_default_file_handler():
	# remove default filer handler created by pyswarms then 
	# add another handler with our desired file path
	logger = logging.getLogger()
	logger.handlers[1].close()
	logger.removeHandler(logger.handlers[1])
	file_path = os.getcwd() + '/log-reports/ps_report.log'
	fmtr = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh = logging.handlers.RotatingFileHandler(file_path, backupCount = 1, mode = 'w')
	fh.setLevel(logging.INFO)
	fh.setFormatter(fmtr)
	logger.addHandler(fh)

def StructureMessage(object):
	def __init__(self, message, *args):
		self.message = message
		self.args = args

	def __str__(self):
		return '%s >>> %s' % ( self.message, ' '.join(map(str, self.args)))

fmt = StructuredMessage

