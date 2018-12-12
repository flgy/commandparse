PYTHON3_BIN = /usr/bin/python3

all: test example

test:
	@pytest-3 -v tests

example:
	$(PYTHON3_BIN) ./example.py info test -o opt -v

clean:
	@find . -name "*.pyc" -delete
	@rm -vrf build/ dist/

release: test
	@python3 setup.py sdist
	@twine upload dist/* --verbose

.PHONY: all test example
