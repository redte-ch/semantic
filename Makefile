.DEFAULT_GOAL := test

clean: $(shell find . -name "*.pyc")
	@rm -rf $?

compile: .
	@python -m compileall -q $?

test: clean compile
	@pytest
