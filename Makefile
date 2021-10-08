.DEFAULT_GOAL := test

install:
	@pip install --upgrade pip wheel setuptools
	@pip install --upgrade poetry

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

test: compile clean
	@poetry run pytest -qx

test-nox:
	@poetry run nox -s test

release:
	@poetry version ${version}
	@git add -A
	@${MAKE} test-nox
	@git commit -m "Bump version to ${version}"
	@git tag ${version}
	@git push --tags
