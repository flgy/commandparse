PYTHON3_BIN = /usr/bin/python3

all: test example

test:
	pytest-3 -v tests

example:
	$(PYTHON3_BIN) ./example.py info test -o opt -v

clean:
	find . -name "*.pyc" -delete


.PHONY: all test example
