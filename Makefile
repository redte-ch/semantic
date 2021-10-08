.DEFAULT_GOAL := test

compile: .
	@python -m compileall -q $?

clean: $(shell find . -name "*.pyc")
	@rm -rf $?

test: compile clean
	@pytest

bump:
	@git tag ${version}
	@git push --tags
