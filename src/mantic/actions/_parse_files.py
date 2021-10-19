# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""File parser.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Any, cast, Generator, Optional, Set, Tuple

import textwrap

import typic

from ..domain import Signature
from ..infra import repo
from ..types import What
from ._build_signatures import BuildSignatures

_this: str = repo.versions.this()
_that: str = repo.versions.last()


@typic.klass(always = True, slots = True, strict = True)
class ParseFiles:
    """Wrapper around the repo and the signature builder.

    Attributes:
        repo: To query files and changes from.
        this: The base revision.
        that: The revision to compare with.
        diff: The list of files changed between ``this`` and ``that``.
        current: ``this`` or ``that``.
        builder: A signature builder.
        signatures: The list of built signatures.

    Args:
        repo: The repo to use, defaults to :class:`.Repo`.
        this: The revision to use, defaults to ``HEAD``.
        that: The revision to compare ``this`` with, defaults to last version.

    Examples:
        >>> parser = ParseFiles(this = "0.3.0", that = "0.2.0")

        >>> parser.diff
        ('.gitignore', '.python-version', '2', 'Makefile', 'noxfile.py', 'p...)

        >>> with parser(what = "this") as parsing:
        ...     list(parsing)
        ...
        [(1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8,...]

        >>> this = set(parser.signatures)

        >>> with parser(what = "that") as parsing:
        ...     list(parsing)
        ...
        [(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9...]

        >>> that = set(parser.signatures)

        >>> with parser(what = "thus") as parsing:
        ...     print("wut!")
        ...
        Traceback (most recent call last):
        AttributeError: 'ParseFiles' object has no attribute 'thus'

        >>> next(iter(this ^ that & this))  # Added functions…
        Signature(name='...', ...

        >>> next(iter(that ^ this & that))  # Removed functions…
        Signature(name='...', ...

    .. versionadded:: 1.0.0

    """

    this: str
    that: str
    current: Optional[str]
    diff: Tuple[str, ...]
    builder: Optional[BuildSignatures]
    signatures: Optional[Tuple[Signature, ...]]

    def __init__(self, *, this: str = _this, that: str = _that) -> None:
        self.this = this
        self.that = that
        self.diff = repo.files.diff(this, that)
        self.current = None
        self.builder = None
        self.signatures = None

    def __call__(self, *, what: What) -> ParseFiles:
        """We try recover the revision (``this`` or ``that``)."""

        # Fails otherwise.
        # pytype: disable=attribute-error
        self.current = self.__getattribute__(what)
        # pytype: enable=attribute-error

        # And we return ourselves.
        return self

    def __enter__(self) -> Generator[Tuple[int, ...], None, None]:
        # We recover the python files corresponding to ``revison``.
        files: Set[str] = {
            file
            for file in repo.files.tree(cast(str, self.current))
            if file.endswith(".py")
            }

        # We only keep the files changed between ``this`` and ``that``.
        to_parse: Set[str] = files & set(self.diff)

        # We create a builder with the selected files.
        self.builder = BuildSignatures(tuple(to_parse))

        # And finally we iterate over the files…
        for file in self.builder.files:

            # We recover the contents of ``file`` at ``revision``.
            content: str = repo.files.show(cast(str, self.current), file)

            # We sanitize the source code.
            source: str = textwrap.dedent(content)

            # Then pass it on to the signature builder.
            self.builder(source)

            # And we yield a counter to keep the user updated.
            yield self.builder.count, self.builder.total

    def __exit__(self, *args: Any) -> None:
        # We save the signatures for upstream recovery.
        self.signatures = cast(BuildSignatures, self.builder).signatures
