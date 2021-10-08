default_session = "test(3.9.7/1.21.2)"

.DEFAULT_GOAL := test

install:
	@pip install --upgrade pip wheel setuptools
	@pip install --upgrade poetry

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

test: compile clean
	@poetry run python -m pysemver CheckVersion
	@poetry run nox -s ${default_session}

release:
	@poetry version ${version}
	@git add -A
	@poetry run nox -s test
	@git commit -m "Bump version to ${version}"
	@git tag ${version}
	@git push --tags
