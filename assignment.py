"""
assignment
Copyright (c) 2016 Angelo Licastro
See LICENSE and README.md.
"""

from os import getcwd

from os.path import isfile
from os.path import join

class Assignment:

    class InvalidAssignmentException(Exception):

        def __init__(self):
            pass

    def __init__(self, id):
        self.id = id

        self.path = join(getcwd(), 'assignments', id)

        self.testsPath = join(self.path, 'tests')
        self.outputsPath = join(self.path, 'outputs')

        self.tests, self.outputs = None, None

        if not isfile(self.testsPath) or not isfile(self.outputsPath):
            raise Assignment.InvalidAssignmentException()

        self._handle()

    def _handle(self):
        """Processes an assignment."""
        with open(self.testsPath) as f:
            contents = f.read()

        contents = contents.split()

        self.tests = ','.join(contents)

        with open(self.outputsPath) as f:
            contents = f.read()

        contents = contents.split()

        self.outputs = ','.join(contents)
