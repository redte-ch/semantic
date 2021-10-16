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

from ._base import run


@deal.has("stdin")
def show(revision: str, file: str, repo: str = "") -> str:
    """Retrives the content of a file in a revision.

    Args:
        revision: A commit, a tag, and so on…
        file: The relative file path.

    Returns:
        str: The contents of the file.

    Examples:
        >>> import os
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> source = show("1.0.0", "func.py", str(repo))
        >>> source
        'def function(a, *, b, c, d):\\n    ...\\n'

    """

    cmd: Sequence[str]
    cmd = ["git", "-C", repo, "show", f"{revision}:{file}"]
    return run(cmd)


@deal.has("stdin")
def tree(revision: str, repo: str = "") -> Sequence[str]:
    """Retrives the list of tracked files in a revision.

    Args:
        revision: A commit, a tag, and so on…

    Returns:
        A sequence with the files' names.

    Examples:
        >>> import os
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> tree("1.0.0", str(repo))
        ['.gitignore', '__init__.py', 'bar.py', 'func.py', 'func_with_chang...]

    .. versionadded:: 1.0.0

    """

    cmd: Sequence[str]
    cmd = ["git", "-C", repo, "ls-tree", "-r", "--name-only", revision]
    return run(cmd).split()


@deal.has("stdin")
def diff(this: str, that: str, repo: str = "") -> Sequence[str]:
    """Retrives the list of changed files between two revisions.

    Args:
        this: A commit, a tag, and so on…
        that: The same as ``that``, but in the past…

    Returns:
        A sequence with the files' names.

    Examples:
        >>> from pathlib import Path

        >>> repo = Path("./tests/fixtures").resolve()
        >>> diff("2.0.0", "1.0.0", str(repo))
        ['func.py']

    .. versionadded:: 1.0.0

    """

    cmd: Sequence[str]
    cmd = ["git", "-C", repo, "diff", "--name-only", f"{that}..{this}"]
    return run(cmd).split()
