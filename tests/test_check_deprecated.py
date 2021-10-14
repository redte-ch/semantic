# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import os
import sys
import tempfile

import pytest

from pysemver._bar import Bar
from pysemver._check_deprecated import CheckDeprecated


class Module:
    """Some module with an expired function."""

    def __init__(self, expires = "never"):
        self.module = [
            b"from openfisca_core.commons import deprecated",
            b"",
            b"",
            f"@deprecated(since = 'today', expires = '{expires}')".encode(),
            b"def function() -> None:",
            b"    ..."
            ]

    def __enter__(self):
        self.file = tempfile.NamedTemporaryFile()
        self.name = ".".join(self.file.name.split("/")[-2:])
        self.file.write(b"\n".join(self.module))
        self.file.seek(0)
        return self.file, self.name

    def __exit__(self, *__):
        self.file.close()


@pytest.fixture
def bar():
    return Bar()


@pytest.fixture
def warn(mocker, bar):
    return mocker.spy(bar, "warn")


@pytest.fixture
def fail(mocker, bar):
    return mocker.spy(bar, "fail")


def test_check_deprecated(warn, bar):
    """Prints out the features marked as deprecated."""

    lineno = 6

    if sys.version_info < (3, 8):
        lineno -= 1

    with Module() as (file, name):
        checker = CheckDeprecated([file.name])
        checker(bar)

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    warn.assert_called()
    assert f"{name}.function:{lineno}" in warn.call_args_list[0][0][0]
    assert exit.value.code == os.EX_OK


def test_find_deprecated_when_expired(fail, bar):
    """Raises an error when at least one deprecation has expired."""

    version = "1.0.0"

    with Module(version) as (file, _):
        checker = CheckDeprecated([file.name], version)
        checker(bar)

    with pytest.raises(SystemExit) as exit:
        sys.exit(checker.exit.value)

    fail.assert_called()
    assert exit.value.code != os.EX_OK
