# Checkmark

Checkmark is a tool that gives students instant feedback on the correctness of their coding assignments.

## Features

* Add new assignments on the fly (no need to restart the server when adding new assignments)
* No arbitrary code execution (all testing is done on the client side)
* No dependencies
* Ready to use out of the box
* Simple UDP protocol

## How does Checkmark work?

Checkmark uses the client-server model. First, the instructor defines the ruleset for the assignment on the server side. Then, the student runs the Checkmark tool on their assignment on the client side. That's it.

## How do I install Checkmark?

Just clone the Checkmark repository. No dependencies required (other than Python, of course).

	$ git clone https://github.com/angelolicastro/checkmark

## How do I set Checkmark up?

There's no set up required. Just run the start script (with the address and port to bind to) on the server side.

	$ checkmark/start.py 0.0.0.0 9999

## How do I use Checkmark?

### Instructor

1. Start the Checkmark server by running the start script.

```
$ cd checkmark
$ ./start.py 0.0.0.0 9999
Listening on 0.0.0.0:9999...
```

2. Create an assignment ruleset by creating a directory for the assignment and the outputs and tests files.

```
$ mkdir assignments
$ cd assignments
$ mkdir 111-01-01
$ cd 111-01-01
$ touch outputs
$ touch tests
```

**Note:** The naming convention for assignments is course-assignment-number.

### Student

1. Create a submission with a docstring that specifies the assignment ID (aid) and student ID (sid).

```
"""
aid = 001-01-01
sid = 100
"""
```

2. Run the Checkmark tool (with the server address and port to connect to) on the submission that you just created.

```
$ ./checkmark.py localhost 9999 test.py
✔ test.py passed 3 out of 3 test cases.
```

**Note:** Tests are performed through command line arguments. If you need help generating a command line argument program for your submission, use [cli-boilerplate-generator](https://github.com/angelolicastro/cli-boilerplate-generator).

## License

[The MIT License (MIT)](LICENSE)

Copyright (c) 2016 [Angelo Licastro](http://angelolicastro.com)
