# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Nox config file."""

from typing import Any, Pattern

import pathlib
import re
import shutil

import nox  # pytype: disable=import-error
import nox_poetry  # pytype: disable=import-error

nox.options.reuse_existing_virtualenvs = True
doc_steps = ("dummy", "doctest", "linkcheck")
doc_build = ("-anqTW", "docs", "docs/_build")
rel_build = ("docs/conf.py", "noxfile.py", "src")
python_versions = ("3.7.9", "3.8.10", "3.9.7")
numpy_versions = ("1.17.5", "1.18.5", "1.19.5", "1.20.3", "1.21.2")
exclude = (("3.9.7", "1.18.5"),)
matrix = tuple(
    (python, numpy)
    for python in python_versions
    for numpy in numpy_versions
    if (python, numpy) not in exclude
    )
ids = tuple(
    f"{python}/{numpy}"
    for python, numpy in matrix
    )


class SessionCache:
    """Class to save/restore poetry settings."""

    sesh_name: str
    sesh_cache: str
    pattern: Pattern = re.compile(r"\(|\)|\/|\=|\'|\"|\,|\s")

    def __init__(self, sesh_name: str, sesh_cache: str) -> None:
        self.lock_name = self.pattern.sub("-", sesh_name)
        self.back_lock = pathlib.Path(f"{sesh_cache}/poetry.lock")
        self.back_toml = pathlib.Path(f"{sesh_cache}/pyproject.toml")
        self.base_lock = pathlib.Path("poetry.lock")
        self.base_toml = pathlib.Path("pyproject.toml")
        self.sesh_lock = pathlib.Path(f"{sesh_cache}/lock-{self.lock_name}")

        if not self.sesh_lock.exists():
            shutil.copyfile(self.base_lock, self.sesh_lock)

    def __enter__(self) -> None:
        shutil.copyfile(self.base_lock, self.back_lock)
        shutil.copyfile(self.base_toml, self.back_toml)
        shutil.copyfile(self.sesh_lock, self.base_lock)

    def __exit__(self, *__: Any) -> None:
        shutil.copyfile(self.base_lock, self.sesh_lock)
        shutil.copyfile(self.back_lock, self.base_lock)
        shutil.copyfile(self.back_toml, self.base_toml)
        self.back_lock.unlink()
        self.back_toml.unlink()


@nox_poetry.session(python = "3.9.7")
def coverage(session) -> None:
    """Run coverage session."""

    # Otherwise the stdout would be cropped.
    env = {"COLUMNS": "200"}

    session.run("make", "install", external = True, silent = True)
    session.install("codecov", silent = True)
    session.install("coverage[toml]", silent = True)
    session.install("pytest", silent = True)
    session.install("pytest-cov", silent = True)
    session.install("pytest-mock", silent = True)
    session.install("pytest-randomly", silent = True)
    session.install("pytest-sugar", silent = True)
    session.install("pytest-xdist", silent = True)
    session.install("robotframework", silent = True)
    session.install("typeguard", silent = True)
    session.install("xdoctest", silent = True)
    session.install(".", silent = True)
    session.run("pytest", "--cov", env = env)
    session.run("robot", "--outputdir", ".robot", "tests/functional")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox_poetry.session(python = "3.9.7")
def docs(session):
    """Build/test docs."""

    session.run("make", "install", external = True, silent = True)
    session.install("interrogate", silent = True)
    session.install("sphinx", silent = True)
    session.install("sphinx-autodoc-typehints", silent = True)
    session.install(".", silent = True)
    session.run("interrogate", "src")

    for step in doc_steps:
        session.run("sphinx-build", "-b", step, *doc_build)


@nox_poetry.session
@nox.parametrize("python", python_versions, ids = python_versions)
def lint(session):
    """Lint files."""

    session.run("make", "install", external = True, silent = True)
    session.install("wemake-python-styleguide", silent = True)
    session.install(".", silent = True)
    session.run("flake8", *(*rel_build, "tests"))


@nox_poetry.session
@nox.parametrize("python, numpy", matrix, ids = ids)
def type(session, numpy):
    """Type-hint code."""

    session.run("make", "install", external = True, silent = True)

    with SessionCache(session.name, session.cache_dir):
        session.run("poetry", "add", f"numpy@{numpy}", silent = True)

    session.install("mypy", silent = True)
    session.install("pytype", silent = True)
    session.install(".", silent = True)
    session.run("mypy", *rel_build)
    session.run("pytype", *rel_build)


@nox_poetry.session
@nox.parametrize("python, numpy", matrix, ids = ids)
def test(session, numpy):
    """Run tests."""

    # Otherwise the stdout would be cropped.
    env = {"COLUMNS": "200"}

    session.run("make", "install", external = True, silent = True)

    with SessionCache(session.name, session.cache_dir):
        session.run("poetry", "add", f"numpy@{numpy}", silent = True)

    session.install("coverage[toml]", silent = True)
    session.install("pytest", silent = True)
    session.install("pytest-cov", silent = True)
    session.install("pytest-mock", silent = True)
    session.install("pytest-randomly", silent = True)
    session.install("pytest-sugar", silent = True)
    session.install("pytest-xdist", silent = True)
    session.install("robotframework", silent = True)
    session.install("typeguard", silent = True)
    session.install("xdoctest", silent = True)
    session.install(".", silent = True)
    session.run("pytest", "--cov", env = env)
    session.run("robot", "--outputdir", ".robot", "tests/functional")
