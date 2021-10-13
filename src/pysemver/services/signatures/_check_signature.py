# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Any, Optional, Protocol, Sequence, Sized, TypeVar

import dataclasses

import deal
import numpy
import typic

from pysemver import utils

from ..._models import Version
from ...domain import Signature

limit = 2e5
"""Just a random size/length sentinel."""


# @typic.al(strict = True)
# @deal.pure
def diff_hash(service: CheckSignature) -> numpy.integer:
    these = utils.fill(service.this_len, service.that_len, service.this)
    those = utils.fill(service.this_len, service.that_len, service.that)

    patch = [
        *
        service.patch,
        *
        repeat(
            service.this_len,
            service.that_len,
            service.patch[0])]
    nones = [
        *
        service.nones,
        *
        repeat(
            service.this_len,
            service.that_len,
            service.nones[0])]

    return numpy.where(these != those, patch, nones)


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
            max(diff_hash(self)),
            max(self.diff_args()),
            max(self.diff_name()),
            max(self.diff_type()),
            max(self.diff_defs()),
            )

    # @deal.pure
    # @typic.al(strict = True)
    def diff_args(self) -> numpy.ndarray:
        these = numpy.array([self.this_len] * self.size_max)
        those = numpy.array([self.that_len] * self.size_max)

        major = [
            *
            self.major,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.major[0])]
        minor = [
            *
            self.minor,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.minor[0])]
        nones = [
            *
            self.nones,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.nones[0])]

        conds = [these < those, these > those, True]
        takes = [major, minor, nones]

        return numpy.select(conds, takes)

    # @deal.pure
    # @typic.al(strict = True)
    def diff_name(self) -> numpy.ndarray:
        these = numpy.array([a.name for a in self.this.arguments])
        those = numpy.array([a.name for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.major, self.nones]

        return [
            *
            numpy.select(
                conds,
                takes),
            *
            repeat(
                self.this_len,
                self.that_len,
                self.minor[0])]

    # @deal.pure
    # @typic.al(strict = True)
    def diff_type(self) -> numpy.ndarray:
        these = numpy.array([a.types is None for a in self.this.arguments])
        those = numpy.array([a.types is None for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.patch, self.nones]

        return [
            *
            numpy.select(
                conds,
                takes),
            *
            repeat(
                self.this_len,
                self.that_len,
                self.nones[0])]

    # @deal.pure
    # @typic.al(strict = True)
    def diff_defs(self) -> numpy.ndarray:
        major = [
            *
            self.major,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.major[0])]
        minor = [
            *
            self.minor,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.minor[0])]
        nones = [
            *
            self.nones,
            *
            repeat(
                self.this_len,
                self.that_len,
                self.nones[0])]

        these = numpy.array(
            [a.default is None for a in self.this.arguments],
            int,
            )

        those = numpy.array(
            [a.default is None for a in self.that.arguments],
            int,
            )

        glued = tuple(zip(
            [*these, *[repeat(self.this_len, self.that_len, self.nones[0]), []][len(these) > len(those)]],
            [*those, *[repeat(self.this_len, self.that_len, self.nones[0]), []][len(those) > len(these)]],
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
