# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Check for signature changes and version bump requirements.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Optional

import dataclasses

import deal
import numpy
import typic

from mantic import utils
from mantic.domain import Signature, VersionInt

limit = 2e5
"""Just a random size/length sentinel."""


@deal.pure
def diff_hash(this: Signature, that: Signature) -> numpy.ndarray:
    """Check if two signatures have a different ``hashes``.

    Args:
        this: A signature.
        that: Another signature.

    Returns:
        numpy.ndarray: An array with the values.

    Examples:
        >>> from mantic.domain import Argument

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

    these = utils.fill(len(this), len(that), abs(hash(this)))
    those = utils.fill(len(this), len(that), abs(hash(that)))
    patch = utils.pop(len(this), len(that), VersionInt.PATCH)
    nones = utils.pop(len(this), len(that), VersionInt.NONE)
    return numpy.where(these != those, patch, nones)


@deal.pure
def diff_args(this: Signature, that: Signature) -> numpy.ndarray:
    """Check if two signatures have a diferent arguments.

    Args:
        this: A signature.
        that: Another signature.

    Returns:
        numpy.ndarray: An array with the values.

    Examples:
        >>> from mantic.domain import Argument

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

        >>> this = Signature("greet", "file.py")

        >>> diff_args(this, that)
        array([3])

        >>> diff_args(that, this)
        array([2])

        >>> that = Signature("greet", "file.py")

        >>> diff_args(this, that)
        array([]...)

        >>> diff_args(that, this)
        array([]...)

    .. versionadded:: 1.0.0

    """

    these = utils.fill(len(this), len(that), len(this))
    those = utils.fill(len(this), len(that), len(that))

    major = utils.pop(len(this), len(that), VersionInt.MAJOR)
    minor = utils.pop(len(this), len(that), VersionInt.MINOR)
    nones = utils.pop(len(this), len(that), VersionInt.NONE)

    conds = [these < those, these > those, True]
    takes = [major, minor, nones]

    return numpy.select(conds, takes)


@deal.pure
def diff_name(this: Signature, that: Signature) -> numpy.ndarray:
    """Check if two signatures have a different argument names.

    Args:
        this: A signature.
        that: Another signature.

    Returns:
        numpy.ndarray: An array with the values.

    Examples:
        >>> from mantic.domain import Argument

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

        >>> this = Signature("greet", "file.py")

        >>> diff_name(this, that)
        array([2])

        >>> diff_name(that, this)
        array([2])

        >>> that = Signature("greet", "file.py")

        >>> diff_name(this, that)
        array([]...)

        >>> diff_name(that, this)
        array([]...)

    .. versionadded:: 1.0.0

    """

    these = numpy.array([a.name for a in this.arguments])
    those = numpy.array([a.name for a in that.arguments])

    # If no arguments, we continue…
    if len(these) == 0 and len(those) == 0:
        return numpy.array([], int)

    # If there are no arguments after, we populate.
    if len(these) == 0:
        these = utils.pop(len(this), len(that), VersionInt.NONE)

    # Inversely as well.
    if len(those) == 0:
        those = utils.pop(len(this), len(that), VersionInt.NONE)

    # We create tuples.
    glued = tuple(zip(these, those))

    # Otherwise we mark missing args after as major.
    conds = [[this != that for this, that in glued], True]
    takes = [
        utils.pre(len(this), len(that), VersionInt.MAJOR),
        utils.pre(len(this), len(that), VersionInt.NONE),
        ]

    # And we mark new args after as minor.
    return numpy.array([
        *numpy.select(conds, takes),
        *utils.rep(len(this), len(that), VersionInt.MINOR),
        ])


@deal.pure
def diff_defs(this: Signature, that: Signature) -> numpy.ndarray:
    """Check if two signatures have a different default values.

    Args:
        this: A signature.
        that: Another signature.

    Returns:
        numpy.ndarray: An array with the values.

    Examples:
        >>> from mantic.domain import Argument

        >>> argument = Argument("count", default = "0")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))

        >>> diff_args(this, that)
        array([0])

        >>> this = Signature("greet", "file.py")

        >>> diff_args(this, that)
        array([3])

        >>> diff_args(that, this)
        array([2])

        >>> that = Signature("greet", "file.py")

        >>> diff_args(this, that)
        array([]...)

        >>> diff_args(that, this)
        array([]...)

    .. versionadded:: 1.0.0

    """

    major = utils.pop(len(this), len(that), VersionInt.MAJOR)
    minor = utils.pop(len(this), len(that), VersionInt.MINOR)
    nones = utils.pop(len(this), len(that), VersionInt.NONE)

    these = numpy.array([a.default is None for a in this.arguments], int)
    those = numpy.array([a.default is None for a in that.arguments], int)

    if len(these) == 0 and len(those) == 0:
        return numpy.array([], int)

    these.resize((major.size,), refcheck = False)
    those.resize((major.size,), refcheck = False)

    glued = tuple(zip(these, those))

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
        >>> from mantic.domain import Argument

        >>> argument = Argument("count")
        >>> this = Signature("greet", "file.py", (argument,))
        >>> that = Signature("greet", "file.py", (argument,))
        >>> service = CheckSignature(this, that)

        >>> service
        CheckSignature(this=Signature(name='greet', file='file.py', argument...

        >>> service.score()
        0

    .. versionadded:: 1.0.0

    """

    this: Signature
    that: Signature
    reason: Optional[str] = None

    def score(self) -> int:
        """Calculates the score, that is the required version bump."""

        hash_score = max(diff_hash(self.this, self.that))
        args_score = max(diff_args(self.this, self.that))
        name_score = max(diff_name(self.this, self.that))
        defs_score = max(diff_defs(self.this, self.that))

        if args_score == 2:
            self.reason = "args-diff"

        if args_score == 3:
            self.reason = "args-diff"

        if name_score == 3:
            self.reason = "args-diff"

        if args_score == 0 and defs_score == 2:
            self.reason = "defaults-diff"

        if args_score == 0 and defs_score == 3:
            self.reason = "defaults-diff"

        if args_score == 2 and defs_score == 0:
            self.reason = "args/defaults-diff"

        return max(hash_score, args_score, name_score, defs_score)
