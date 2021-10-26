# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

.DEFAULT_GOAL := all

all: format bind lint type test ;

%:
	@${MAKE} bind-$*
	@${MAKE} lint-$*
	@${MAKE} type-$*
	@${MAKE} test-$*

install:
	@python -m pip install --upgrade pip wheel setuptools
	@python -m pip install --upgrade nox-poetry
	@python -m pip install --upgrade poetry
	@python -m pip install --upgrade nox

compile: src
	@poetry run python -m compileall -q $?

clean: src
	@rm -rf $(shell find $? -name "*.pyc")

format: $(shell git ls-files "*.py")
	@poetry run isort $?
	@poetry run autopep8 $?
	@poetry run pyupgrade $? --py36-plus --keep-runtime-typing

bind: compile clean
	@poetry run python -m deal test --count=25 src

bind-%: compile clean
	@poetry run python -m deal test --count=100 src/$*

lint: compile clean
	@poetry run flake8 docs/conf.py src tests noxfile.py
	@poetry run sphinx-build -b dummy -anqTW docs docs/_build

lint-%: compile clean
	@poetry run flake8 src/$*

type: compile clean
	@poetry run mypy docs/conf.py src noxfile.py
	@poetry run pytype docs/conf.py src noxfile.py

type-%: compile clean
	@poetry run mypy src/$*
	@poetry run pytype src/$*

test: export COLUMNS = 200
test: compile clean
	@poetry run pytest --cov
	@poetry run robot --outputdir .robot tests/functional
	@poetry run interrogate src
	@poetry run sphinx-build -b doctest -anqTW docs docs/_build

test-%: export COLUMNS = 200
test-%: compile clean
	@poetry run pytest src/$*
	@poetry run interrogate src/$*

tag-version:
	@poetry version --short | xargs -I \{\} git tag \{\}
	@git push --tags

bump-version:
	@poetry run pip uninstall mantic -y -q
	@poetry install -q
	@poetry run mantic check-version \
		&& exit_code=$${?} \
		|| exit_code=$${?} \
		&& version=( "" "patch" "minor" "major" ) \
		&& poetry version $${version[$${exit_code}]} -q \
		&& poetry install -q \
		&& git add -A \
		&& poetry version --short | xargs -I \{\} git commit -m "Bump version to {}" \
		&& git push origin $(shell git branch --show-current)
