# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Retrieves file/change information.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Sequence

import deal

from . import _repo


@deal.pure
def show(revision: str, file: str) -> str:
    """Retrives the content of a file in a revision.

    Args:
        revision: A commit, a tag, and so on…
        file: The relative file path.

    Returns:
        str: The contents of the file.

    Examples:
        >>> source = Repo.File.show(
        ...     "0.5.0",
        ...     "openfisca_core/calmar.py",
        ...     )
        >>> source.split("\\n")[3]
        '# OpenFisca -- A versatile microsimulation software'

    """

    cmd: Sequence[str]
    cmd = ["git", "show", f"{revision}:{file}"]
    return _repo.run(cmd)


@deal.pure
def tree(revision: str) -> Sequence[str]:
    """Retrives the list of tracked files in a revision.

    Args:
        revision: A commit, a tag, and so on…

    Returns:
        A sequence with the files' names.

    Examples:
        >>> Repo.File.tree("0.5.0")[13]
        'openfisca_core/calmar.py'

    .. versionadded:: 36.1.0

    """

    cmd: Sequence[str]
    cmd = ["git", "ls-tree", "-r", "--name-only", revision]
    return _repo.run(cmd).split()


@deal.pure
def diff(this: str, that: str) -> Sequence[str]:
    """Retrives the list of changed files between two revisions.

    Args:
        this: A commit, a tag, and so on…
        that: The same as ``that``, but in the past…

    Returns:
        A sequence with the files' names.

    Examples:
        >>> Repo.File.diff("0.5.0", "0.5.1")
        ['.travis.yml', 'CHANGELOG.md', 'COPYING', 'Makefile', 'READ...

    .. versionadded:: 36.1.0

    """

    cmd: Sequence[str]
    cmd = ["git", "diff", "--name-only", f"{that}..{this}"]
    return _repo.run(cmd).split()
