#!/usr/bin/env python3

"""
start
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

from argparse import ArgumentParser

from server import Server

def main():
	argumentParser = ArgumentParser()

	argumentParser.add_argument('address')
	argumentParser.add_argument('port', type=int)

	arguments = argumentParser.parse_args()

	server = Server(arguments.address, arguments.port)

if __name__ == '__main__':
	main()
