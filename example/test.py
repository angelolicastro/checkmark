"""
aid = 001-01-01
sid = 1
"""

from argparse import ArgumentParser

def square(n):
    return n * n

def main():
    argumentParser = ArgumentParser()
    argumentParser.add_argument('n', type=int)
    arguments = argumentParser.parse_args()
    print(square(arguments.n))

if __name__ == '__main__':
    main()
