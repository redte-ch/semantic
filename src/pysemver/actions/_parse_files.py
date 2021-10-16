# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Any, Generator, Optional, Sequence, Set, Tuple

import textwrap

import deal
import typic

from ..domain import Signature
from ..infra.repo import files, versions
from ..types import What
from ._build_signatures import SignatureBuilder

THIS: str = versions.this()
THAT: str = versions.last()


# @typic.klass(always = True, slots = True, strict = True)
class Parser:
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
        >>> parser = Parser(this = "0.4.0", that = "0.2.0")

        >>> parser.diff
        ['.gitignore', '.python-version', 'Makefile', 'noxfile.py', 'poetry...

        >>> with parser(what = "this") as parsing:
        ...     list(parsing)
        ...
        [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)]

        >>> this = set(parser.signatures)

        >>> with parser(what = "that") as parsing:
        ...     list(parsing)
        ...
        [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]

        >>> that = set(parser.signatures)

        >>> with parser(what = "thus") as parsing:
        ...     print("wut!")
        ...
        Traceback (most recent call last):
        AttributeError: 'Parser' object has no attribute 'thus'

        >>> next(iter(this ^ that & this))  # Added functions…
        Signature(name='...', ...

        >>> next(iter(that ^ this & that))  # Removed functions…
        Signature(name='...', ...

    .. versionadded:: 36.1.0

    """

    this: str
    that: str
    current: Optional[str]
    diff: Sequence[str]
    builder: Optional[SignatureBuilder]
    signatures: Optional[Sequence[Signature]]

    # @deal.pure
    # @typic.al(strict = True)
    def __init__(self, *, this: str = THIS, that: str = THAT) -> None:
        self.this = this
        self.that = that
        self.diff = files.diff(this, that)
        self.current = None
        self.builder = None
        self.signatures = None

    # @deal.pure
    # @typic.al(strict = True)
    def __call__(self, *, what: What) -> Parser:
        # We try recover the revision (``this`` or ``that``). Fails otherwise.
        self.current: str = self.__getattribute__(what)

        # And we return ourselves.
        return self

    # @deal.pure
    def __enter__(self) -> Generator[Tuple[int, ...], None, None]:
        # We recover the python files corresponding to ``revison``.
        files: Set[str] = {
            file
            for file in files.tree(self.current)
            if file.endswith(".py")
            }

        # We only keep the files changed between ``this`` and ``that``.
        to_parse: Set[str] = files & set(self.diff)

        # We create a builder with the selected files.
        self.builder: SignatureBuilder(tuple(to_parse))

        # And finally we iterate over the files…
        for file in self.builder.files:

            # We recover the contents of ``file`` at ``revision``.
            content: str = files.show(self.current, file)

            # We sanitize the source code.
            source: str = textwrap.dedent(content)

            # Then pass it on to the signature builder.
            self.builder(source)

            # And we yield a counter to keep the user updated.
            yield self.builder.count, self.builder.total

    # @deal.pure
    def __exit__(self, *__: Any) -> None:
        # We save the signatures for upstream recovery.
        self.signatures = self.builder.signatures
