.DEFAULT_GOAL := test

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

test: compile clean
	@poetry run pytest -qx

test-nox: \
	test-nox-3.7.11 \
	test-nox-3.8.12 \
	test-nox-3.9.7 \
	test-nox-3.10.0 \
	;

test-nox-%:
	@poetry run nox -p $*

version:
	@git tag ${version}
	@git push --tags
