# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""PySemver's version bumper tests.

.. versionadded:: 1.2.0

"""

import pytest

from mantic.actions._bump_version import BumpVersion
from mantic.domain import VersionInt


@pytest.fixture
def bump_version():
    return BumpVersion(this = "1.2.3", that = "1.2.3")


def test_is_acceptable_when_no_bump_is_required(bump_version):
    assert bump_version.is_acceptable()


def test_is_acceptable_when_patch_is_required(bump_version):
    bump_version(VersionInt.PATCH)
    assert not bump_version.is_acceptable()

    bump_version.this = "1.2.4"
    assert bump_version.is_acceptable()

    bump_version.this = "1.3.0"
    assert bump_version.is_acceptable()

    bump_version.this = "2.0.0"
    assert bump_version.is_acceptable()


def test_is_acceptable_when_minor_is_required(bump_version):
    bump_version(VersionInt.MINOR)
    assert not bump_version.is_acceptable()

    bump_version.this = "1.2.4"
    assert not bump_version.is_acceptable()

    bump_version.this = "1.3.0"
    assert bump_version.is_acceptable()

    bump_version.this = "2.0.0"
    assert bump_version.is_acceptable()


def test_is_acceptable_when_major_is_required(bump_version):
    bump_version(VersionInt.MAJOR)
    assert not bump_version.is_acceptable()

    bump_version.this = "1.2.4"
    assert not bump_version.is_acceptable()

    bump_version.this = "1.3.0"
    assert not bump_version.is_acceptable()

    bump_version.this = "2.0.0"
    assert bump_version.is_acceptable()
