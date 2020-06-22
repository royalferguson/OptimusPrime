import pickle
import logging
import logging.handlers
import socketserver
import struct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading, time
import os
import argparse
from OptimusPrime.utils.io.pickleType import read_from_pickle
from OptimusPrime.utils.display import set_global_frame,start_display_window
import json

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
	'''
	Handler for streaming logging request
	Continuously receives and decodes messages for the visualizer to be displayed.
	'''

	def handle(self):
		'''
		Handle multiple requests - each expected to be a 4 byte length
		followed by the LogRecord in pickle format.  Logs the record 
		according to whatever policyis configured locally
		'''
		while True:
			chunk = self.connection.recv(4)
			if len(chunk) < 5:
				break
			slen = struct.unpack('>L', chunk)[0]
			chunk = self.connection.recv(slen)
			while len(chunk) < slen:
				chunk = chunk + self.connection.recv(slen - len(chunk))
			obj = self.unPickle(chunk)
			record = logging.makeLogRecord(obj)
			self.handleLogRecord(record)

	def unPickle(self,data):
		return pickle.loads(data)

	def handleLogRecord(self, record):
		v= Visualizer.getInstance()
		v.handleRecord(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
	'''
	Simple TCP socket-based logging receiver suitable for testing.
	Sets up the communication connection between the visualizer and logger
	Keeps the connection between the two until interrupted.
	'''
	allow_reuse_address = True
	daemon_threads=True		# Decides how threads will act upon termination of the main process

	def __init__(self, host='localhost', port=logging.handlers.DEFAULT_TCP_LOGGING_PORT, handler=LogRecordStreamHandler):
		socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
		self.abort = 0
		self.timeout = 1
		self.logname = None

	def serve_until_stopped(self):
		import select
		abort = 0
		while not abort:
			rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
			if rd:
				self.handle_request()
			abort = self.abort

class Visualizer():
	'''
	Class used for displaying the results of Optimus
	'''
	__instance = None
	@staticmethod
	def getInstance():
		# Static Access Method
		if Visualizer.__instance == None:
			Visualizer()
		return Visualizer.__instance

	def __init__(self):
		# vitually private constructor
		if Visualizer.__instance != None:
			raise Exception("This class is a singleton")
		else:
			Visualizer.__instance = self
		self.log_receiver = None
		self.log_rcv_th = None
		self.file_path = None
		self.intermitent_data = pd.DataFrame()

	def finish_init(self, host='localhost', file = None):
		''' 
		Two Part Initializaton
		This should be called after initial get instance is called to finish the initialization
		'''
		self.log_receiver = LogRecordSocketReceiver(host=host)
		self.log_rcv_th = threading.Thread(target=self.log_receiver.serve_forever)
		self.file_path = file

	def handleRecord(self, record):
		# Callback function used by LogRecordSocketReceiver
		msg = record.getMessage()
		data = json.loads(msg)   # get json from the string
		series = pd.Series(data)    # get the series for the json
		self.intermitent_data = self.intermitent_data_append(series, ignore_index = True)

	def start_receiving(self):
		# start log_receiver.serve_forever in another thread 
		print("Starting log_receiver.serve_forever")
		self.log_rcv_th.start()

	def read_file(self):
		# reads the otpimization data from the file set by the command line
		if self.file_path:
			print('reading from ' + os.path.abspath(self.file_path))
			d = pd.DataFrame()
			for item in read_from_pickle(self.file_path):
				d = d.append(item, ignore_index = True)
			self.intermitent_data = d
			print(d.shape)
		else:
			print("file path not set")

	def stop_receiving(self):
		self.log_receiver.shutdown()
		self.log_receiver.server_close()
		self.log_rcv_th.join()

def is_path(string):
		#Verify valid file path
	if os.path.exists(string):
		return string
	else:
		raise NotADirectoryError(string)

def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument('-f', '--file', nargs=1, type=is_path, help='provide path to file for visulaizer to read them')
	group.add_argument('-n', '--network', nargs='?', const='localhost', help='provide network for visualizer to recieve from optimus')
	args = parser.parse_args()

	v = Visualizer.getInstance()

	if args.file:
		v.finish_init(file=args.file[0])
		v.read_file()
		set_global_frame(v.intermitent_data)
	elif args.network:
		v.finish_init(host=args.network)
		v.start_receiving()
	start_display_window()
if __name__ == '__main__':
	main()



