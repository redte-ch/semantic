.DEFAULT_GOAL := test

install:
	@pip install --upgrade pip poetry
	@poetry install

compile: .
	@python -m compileall -q $?

clean: $(shell find . -name "*.pyc")
	@rm -rf $?

test: compile clean
	@pytest

bump:
	@git tag ${version}
	@git push --tags
