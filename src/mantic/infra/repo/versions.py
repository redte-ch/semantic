# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Retrieves version/change information.

.. versionadded:: 1.0.0

"""


from __future__ import annotations

import deal
import pkg_resources
from git import Repo


@deal.pure
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

    return (
        pkg_resources
        .get_distribution("mantic")
        .version
        )


@deal.pure
def last(repo: str = "") -> str:
    """Retrives the last tagged version.

    Args:
        repo: The git repository path.

    Returns:
        str: Representing the version.

    Examples:
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> last(str(repo))
        '10.0.0'

    .. versionadded:: 1.0.0

    """

    return (
        Repo(repo)
        .git
        .describe("--tags", "--abbrev=0", "--first-parent")
        .split()[0]
        )
