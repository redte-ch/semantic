# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

.DEFAULT_GOAL := all

all: format bind lint type test ;

install:
	@pip install --upgrade pip wheel setuptools
	@pip install --upgrade nox-poetry
	@pip install --upgrade poetry
	@pip install --upgrade nox

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

format: $(shell git ls-files "*.py")
	@poetry run isort $?
	@poetry run autopep8 $?
	@poetry run pyupgrade $? --py36-plus --keep-runtime-typing

bind: compile clean
	@poetry run python -m deal test --count=100 src
	@poetry run crosshair check src

lint: compile clean
	@poetry run flake8 docs/conf.py src tests noxfile.py
	@poetry run sphinx-build -b dummy -anqTW docs docs/_build

type: compile clean
	@poetry run mypy docs/conf.py src noxfile.py
	@poetry run pytype docs/conf.py src noxfile.py

test: compile clean
	@poetry run robot --maxerrorlines NONE tests/functional
	@poetry run pytest --cov
	@poetry run interrogate src
	@poetry run sphinx-build -b doctest -anqTW docs docs/_build

release:
	@nox -k "not coverage"
	@poetry run pip uninstall pysemver -y -q
	@poetry install -q
	@poetry run pysemver check-version \
		&& exit_code=$${?} \
		|| exit_code=$${?} \
		&& version=( "" "patch" "minor" "major" ) \
		&& poetry version $${version[$${exit_code}]} -q \
		&& poetry install -q \
		&& git add -A \
		&& poetry version --short | xargs -I \{\} git commit -m "Bump version to {}" \
		&& poetry version --short | xargs -I \{\} git tag \{\} \
		&& git push --tags
