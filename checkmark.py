#!/usr/bin/env python3

"""
checkmark
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

from argparse import ArgumentParser

from os import getcwd

from os.path import isfile
from os.path import join
from os.path import splitext

from re import DOTALL
from re import match as re_match

from socket import AF_INET
from socket import SOCK_DGRAM
from socket import socket

from subprocess import CalledProcessError
from subprocess import PIPE
from subprocess import run

LANGUAGE_CONFIGURATION = {
	'py': {
		'command': 'python3',
		'commentPattern': '\"\"\".+\"\"\"'
	}
}

def main():
	argumentParser = ArgumentParser()

	argumentParser.add_argument('address')
	argumentParser.add_argument('port', type=int)
	argumentParser.add_argument('filename')

	arguments = argumentParser.parse_args()

	filePath = join(getcwd(), arguments.filename)

	try:
		extension = splitext(arguments.filename)[1][1:]
		command = LANGUAGE_CONFIGURATION[extension]['command']
		commentPattern = LANGUAGE_CONFIGURATION[extension]['commentPattern']

	except KeyError:
		return

	try:
		submission = Submission(filePath, commentPattern)

	except Submission.InvalidSubmissionException:
		return

	try:
		request = Request(arguments.address, arguments.port, '1 {0} {1} XXX' \
			.format(submission.sid, submission.aid))

	except Request.InvalidRequestException:
		return

	tests = list(map(int, request.tests.split(',')))

	try:
		tests = [Test(command, filePath, test) for test in tests]

	except Test.InvalidTestException:
		return

	results = [test.result for test in tests]

	results = ','.join(results)

	request = Request(arguments.address, arguments.port, '2 {0} {1} {2}'\
		.format(submission.sid, submission.aid, results))

	passed = int(request.passed)
	testsLength = len(tests)

	print('{0} {1} passed {2} out of {3} test cases.' \
		.format('✔' if passed == testsLength else '✘', arguments.filename, passed, \
		testsLength))

def aggregate(data):
	"""Aggregates keys and data as a dict."""
	keys = ['mid', 'sid', 'aid', 'msg']
	return dict(zip(keys, data))

class Request:

	class InvalidRequestException(Exception):

		def __init__(self):
			pass

	def __init__(self, address, port, data):
		self.address, self.port, self.data = address, port, data

		self.socket = socket(AF_INET, SOCK_DGRAM)
		self.socket.connect((self.address, self.port))

		self._send()

	def _handle(self):
		"""Processes a single request."""
		data = aggregate(self.data.split())
		received = aggregate(self.received.split())
		if received['mid'] != data['mid']:
			raise Request.InvalidRequestException()
		elif received['sid'] != data['sid']:
			raise Request.InvalidRequestException()
		elif received['aid'] != data['aid']:
			raise Request.InvalidRequestException()
		elif received['mid'] == '1':
			self.tests = received['msg']
		elif received['mid'] == '2':
			self.passed = received['msg']

	def _send(self):
		"""Sends requests to the server."""
		data = bytes(self.data, 'utf-8')
		self.socket.send(data)
		self.received = str(self.socket.recv(1024), 'utf-8')
		self.socket.close()
		self._handle()

class Submission:

	class InvalidSubmissionException(Exception):

		def __init__(self):
			pass

	def __init__(self, filename, commentPattern):
		self.filename, self.commentPattern = filename, commentPattern

		self.aid, self.sid = None, None

		if not isfile(filename):
			raise Submission.InvalidSubmissionException()
		self._parse()

	def _parse(self):
		"""Parses the submission file."""
		with open(self.filename, 'r') as f:
			contents = f.read()
		match = re_match(self.commentPattern, contents, DOTALL)
		start, end = match.start(0), match.end(0)
		data = contents[start + 3:end - 3].strip()
		data = data.split()
		data = dict(zip(data[0::3], data[2::3]))
		self.aid, self.sid = data['aid'], data['sid']

class Test:

	class InvalidTestException(Exception):

		def __init__(self):
			pass

	def __init__(self, command, filename, arguments):
		self.command, self.filename, self.arguments = command, filename, arguments
		self.result = None
		self._run()

	def _run(self):
		"""Runs the test."""
		try:
			self.result = run('{0} {1} {2}'.format(self.command, self.filename, \
				self.arguments), check=True, shell=True, stdout=PIPE).stdout \
				.decode('utf-8').strip()
		except CalledProcessError:
			raise Test.InvalidTestException()

if __name__ == '__main__':
	main()
