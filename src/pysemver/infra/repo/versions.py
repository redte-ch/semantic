# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Retrieves version/change information.

.. versionadded:: 1.0.0

"""


from __future__ import annotations

from typing import Sequence

import deal
import pkg_resources

from ._base import run


# @deal.pure
def this() -> str:
    """Retrives the actual version.

    Returns:
        str: Representing the version.

    Examples:
        >>> version = this()
        >>> major, minor, patch, *rest = version.split(".")
        >>> major.isdecimal()
        True

    .. versionadded:: 1.0.0

    """

    # TODO: This needs to go to a config, or something.

    return (
        pkg_resources
        .get_distribution("pysemver")
        .version
        )


# @deal.pure
def last() -> str:
    """Retrives the last tagged version.

    Returns:
        str: Representing the version.

    Examples:
        >>> version = last()
        >>> major, minor, patch, *rest = version.split(".")
        >>> major.isdecimal()
        True

    .. versionadded:: 1.0.0

    """

    cmd: Sequence[str]
    cmd = ["git", "describe", "--tags", "--abbrev=0", "--first-parent"]
    return run(cmd).split()[0]
