"""
server
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

from assignment import Assignment

from socket import AF_INET
from socket import SOCK_DGRAM
from socket import socket

class Server:

	def __init__(self, address, port):
		self.address, self.port = address, port

		self.socket = socket(AF_INET, SOCK_DGRAM)
		self.socket.bind((self.address, self.port))

		self._serve()

	def _aggregate(data):
		"""Aggregates keys and data as a dict."""
		keys = ['mid', 'sid', 'aid', 'msg']
		return dict(zip(keys, data.split()))

	def _handle(data):
		"""Processes a single request."""
		data = Server._aggregate(data)
		mid = int(data['mid'])
		if mid > 0 and mid < 3:
			try:
				assignment = Assignment(data['aid'])
			except Assignment.InvalidAssignmentException:
				return '3 {0} {1} XXX'.format(data['sid'], data['aid'])
		if mid == 1:
			return '1 {0} {1} {2}'.format(data['sid'], data['aid'], assignment.tests)
		if mid == 2:
			results = data['msg'].split(',')
			outputs = assignment.outputs.split(',')
			passed  = sum([1 if results[i] == outputs[i] else 0 for i in range(len(results))])
			return '2 {0} {1} {2}'.format(data['sid'], data['aid'], passed)

	def _serve(self):
		"""Handles requests forever."""
		print('Listening on {0}:{1}...'.format(self.address, self.port))
		while True:
			data, address = self.socket.recvfrom(1024)
			data = data.decode('utf-8')
			data = Server._handle(data)
			data = data.encode('utf-8')
			self.socket.sendto(data, address)
