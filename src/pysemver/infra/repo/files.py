# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Retrieves file/change information.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Tuple

import deal
from git import Repo
from git.exc import GitCommandError


@deal.pre(lambda _: len(_.revision) > 0 and len(_.file) > 0)
@deal.raises(TypeError, ValueError)
@deal.has("io")
def show(revision: str, file: str, repo: str = "") -> str:
    """Retrives the content of a file in a revision.

    Args:
        revision: A commit, a tag, and so on…
        file: The relative file path.
        repo: The git repository path.

    Returns:
        str: The contents of the file.

    Raises:
        TypeError: When arguments are invalid.

    Examples:
        >>> import os
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> source = show("1.0.0", "func.py", str(repo))
        >>> source
        'def function(a, *, b, c, d):\\n    ...'

    .. versionadded:: 1.0.0

    """

    try:
        return (
            Repo(repo)
            .git
            .show(f"{revision}:{file}")
            )
    except GitCommandError as error:
        raise TypeError(error) from error


@deal.pre(lambda _: len(_.revision) > 0)
@deal.raises(TypeError, ValueError)
@deal.has("io")
def tree(revision: str, repo: str = "") -> Tuple[str, ...]:
    """Retrives the list of tracked files in a revision.

    Args:
        revision: A commit, a tag, and so on…
        repo: The git repository path.

    Returns:
        A sequence with the files' names.

    Raises:
        TypeError: When arguments are invalid.

    Examples:
        >>> import os
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> tree("1.0.0", str(repo))
        ('.gitignore', '__init__.py', 'bar.py', 'func.py', 'func_with_chang...)

    .. versionadded:: 1.0.0

    """
    try:
        return tuple(
            Repo(repo)
            .git
            .ls_tree("-r", "--name-only", revision)
            .split()
            )
    except GitCommandError as error:
        raise TypeError(error) from error


@deal.pre(lambda _: len(_.this) > 0 and len(_.that) > 0)
@deal.raises(TypeError, ValueError)
@deal.has("io")
def diff(this: str, that: str, repo: str = "") -> Tuple[str, ...]:
    """Retrives the list of changed files between two revisions.

    Args:
        this: A commit, a tag, and so on…
        that: The same as ``that``, but in the past…
        repo: The git repository path.

    Returns:
        A sequence with the files' names.

    Raises:
        TypeError: When arguments are invalid.

    Examples:
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> diff("2.0.0", "1.0.0", str(repo))
        ('func.py',)

    .. versionadded:: 1.0.0

    """

    try:
        return tuple(
            Repo(repo)
            .git
            .diff("--name-only", f"{that}..{this}")
            .split()
            )
    except GitCommandError as error:
        raise TypeError(error) from error
