# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Check for signature changes and version bump requirements."""

from __future__ import annotations

from typing import Optional

import dataclasses

import deal
import numpy
import typic

from .. import utils
from ..domain import Signature, Version

limit = 2e5
"""Just a random size/length sentinel."""


@deal.pure
def diff_hash(this: DataclassLike, that: DataclassLike) -> numpy.ndarray:
    """Check if two signatures have a different ``hashes``.

    Args:
        this: A signature.
        that: Another signature.

    Examples:
        >>> from pysemver.domain import Argument

        >>> argument = Argument("count", default = "0")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))

        >>> diff_hash(this, that)
        array([0])

        >>> argument = Argument("count")
        >>> this = Signature("greet", "file.py", (argument,))

        >>> diff_hash(this, that)
        array([1])

        >>> diff_hash(that, this)
        array([1])

    .. versionadded:: 1.0.0

    """

    these = utils.fill(len(this), len(that), this)
    those = utils.fill(len(this), len(that), that)
    patch = utils.pop(len(this), len(that), Version.Int.PATCH)
    nones = utils.pop(len(this), len(that), Version.Int.NONE)
    return numpy.where(these != those, patch, nones)


@deal.pure
def diff_args(this: DataclassLike, that: DataclassLike) -> numpy.ndarray:
    """Check if two signatures have a diferent arguments.

    Args:
        this: A signature.
        that: Another signature.

    Examples:
        >>> from pysemver.domain import Argument

        >>> argument = Argument("count", default = "0")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))

        >>> diff_args(this, that)
        array([0])

        >>> another_argument = Argument("size")
        >>> this = Signature("greet", "file.py", (argument, another_argument))

        >>> diff_args(this, that)
        array([2, 2])

        >>> diff_args(that, this)
        array([3, 3])

    .. versionadded:: 1.0.0

    """

    these = utils.fill(len(this), len(that), len(this))
    those = utils.fill(len(this), len(that), len(that))

    major = utils.pop(len(this), len(that), Version.Int.MAJOR)
    minor = utils.pop(len(this), len(that), Version.Int.MINOR)
    nones = utils.pop(len(this), len(that), Version.Int.NONE)

    conds = [these < those, these > those, True]
    takes = [major, minor, nones]

    return numpy.select(conds, takes)


@deal.pure
def diff_name(this: DataclassLike, that: DataclassLike) -> numpy.ndarray:
    """Check if two signatures have a different argument names.

    Args:
        this: A signature.
        that: Another signature.

    Examples:
        >>> from pysemver.domain import Argument

        >>> argument = Argument("count")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))

        >>> diff_name(this, that)
        array([0])

        >>> another_argument = Argument("size")
        >>> this = Signature("greet", "file.py", (argument, another_argument))

        >>> diff_name(this, that)
        array([0, 2])

        >>> diff_name(that, this)
        array([0, 2])

        >>> argument = Argument("counter")
        >>> this = Signature("greet", "file.py", (argument,))

        >>> diff_name(this, that)
        array([3])

        >>> diff_name(that, this)
        array([3])

    .. versionadded:: 1.0.0

    """

    these = numpy.array([a.name for a in this.arguments])
    those = numpy.array([a.name for a in that.arguments])
    glued = tuple(zip(these, those))

    conds = [[this != that for this, that in glued], True]
    takes = [
        utils.pre(len(this), len(that), Version.Int.MAJOR),
        utils.pre(len(this), len(that), Version.Int.NONE),
        ]

    return numpy.array([
        *numpy.select(conds, takes),
        *utils.rep(len(this), len(that), Version.Int.MINOR),
        ])


@deal.pure
def diff_type(this: DataclassLike, that: DataclassLike) -> numpy.ndarray:
    """Check if two signatures have a different types.

    Args:
        this: A signature.
        that: Another signature.

    Examples:
        >>> from pysemver.domain import Argument

        >>> argument = Argument("count")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))

        >>> diff_type(this, that)
        array([0])

        >>> argument = Argument("count", types = ("List", "int"))
        >>> this = Signature("greet", "file.py", (argument,))

        >>> diff_type(this, that)
        array([1])

        >>> diff_type(that, this)
        array([1])

    .. versionadded:: 1.0.0

    """

    these = numpy.array([a.types is None for a in this.arguments])
    those = numpy.array([a.types is None for a in that.arguments])
    glued = tuple(zip(these, those))

    conds = [[this != that for this, that in glued], True]
    takes = [
        utils.pre(len(this), len(that), Version.Int.PATCH),
        utils.pre(len(this), len(that), Version.Int.NONE),
        ]

    return numpy.array([
        *numpy.select(conds, takes),
        *utils.rep(len(this), len(that), Version.Int.NONE),
        ])


@deal.pure
def diff_defs(this: DataclassLike, that: DataclassLike) -> numpy.ndarray:
    major = utils.pop(len(this), len(that), Version.Int.MAJOR)
    minor = utils.pop(len(this), len(that), Version.Int.MINOR)
    nones = utils.pop(len(this), len(that), Version.Int.NONE)

    these = numpy.array([a.default is None for a in this.arguments], int)
    those = numpy.array([a.default is None for a in that.arguments], int)

    glued = tuple(zip(
        [*these, *[utils.rep(len(this), len(that), Version.Int.NONE), []][len(these) > len(those)]],
        [*those, *[utils.rep(len(this), len(that), Version.Int.NONE), []][len(those) > len(these)]],
        ))

    conds = [
        [this > that for this, that in glued],
        [this < that for this, that in glued],
        True,
        ]

    takes = [
        major,
        minor,
        nones,
        ]

    return numpy.select(conds, takes)


@typic.klass(always = True, slots = True, strict = True)
@dataclasses.dataclass
class CheckSignature:
    """Checks for changes between two :class:`.Signature`.

    Args:
        this: A signature.
        that: Another signature.

    Examples
        >>> from pysemver.domain import Argument

        >>> argument = Argument("count")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))
        >>> service = CheckSignature(this, that)

        >>> service
        CheckSignature(this=Signature(name='greet', file='file.py', argument...

        >>> service.score()
        0

    """

    this: Signature
    that: Signature
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        self.this_len: int = len(self.this.arguments)
        self.that_len: int = len(self.that.arguments)
        self.size_max: int = max(self.this_len, self.that_len)
        self.size_min: int = min(self.this_len, self.that_len)

    # @deal.pure
    # @typic.al(strict = True)
    @property
    def nones(self) -> numpy.ndarray:
        return numpy.repeat(Version.Int.NONE.value, self.size_min)

    # @deal.pure
    # @typic.al(strict = True)
    @property
    def patch(self) -> numpy.ndarray:
        return numpy.repeat(Version.Int.PATCH.value, self.size_min)

    # @deal.pure
    # @typic.al(strict = True)
    @property
    def minor(self) -> numpy.ndarray:
        return numpy.repeat(Version.Int.MINOR.value, self.size_min)

    # @deal.pure
    # @typic.al(strict = True)
    @property
    def major(self) -> numpy.ndarray:
        return numpy.repeat(Version.Int.MAJOR.value, self.size_min)

    # @deal.pure
    # @typic.al(strict = True)

    # @deal.pure
    # @typic.al(strict = True)
    def score(self) -> int:
        if max(self.diff_args()) == 2:
            self.reason = "args-diff"

        if max(self.diff_args()) == 3:
            self.reason = "args-diff"

        if max(self.diff_name()) == 3:
            self.reason = "args-diff"

        if max(self.diff_type()) == 1:
            self.reason = "types-diff"

        if max(self.diff_args()) == 0 and max(self.diff_defs()) == 2:
            self.reason = "defaults-diff"

        if max(self.diff_args()) == 0 and max(self.diff_defs()) == 3:
            self.reason = "defaults-diff"

        if max(self.diff_args()) == 2 and max(self.diff_defs()) == 0:
            self.reason = "args/defaults-diff"

        return max(
            max(diff_hash(self.this, self.that)),
            max(diff_args(self.this, self.that)),
            max(diff_name(self.this, self.that)),
            max(diff_type(self.this, self.that)),
            max(diff_defs(self.this, self.that)),
            )
