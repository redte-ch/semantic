# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from typing import Optional

import deal
import numpy
import typic

from ._models import Signature


@typic.klass(always = True, slots = True, strict = True)
class FuncChecker:

    this: Signature
    that: Signature
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        self.this_len: int = len(self.this.arguments)
        self.that_len: int = len(self.that.arguments)
        self.this_add: int = max(self.that_len - self.this_len, 0)
        self.that_add: int = max(self.this_len - self.that_len, 0)
        self.size_max: int = max(self.this_len, self.that_len)
        self.size_min: int = min(self.this_len, self.that_len)

    @property
    @deal.pure
    def nones(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.NONES.value, self.size_min)

    @property
    @deal.pure
    def patch(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.PATCH.value, self.size_min)

    @property
    @deal.pure
    def minor(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.MINOR.value, self.size_min)

    @property
    @deal.pure
    def major(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.MAJOR.value, self.size_min)

    @deal.pure
    @typic.al(strict = True)
    def filler(self, array: numpy.ndarray) -> numpy.ndarray:
        index: int = array[0]
        times: int = max(self.this_add, self.that_add)

        return numpy.repeat(index, times)

    @deal.pure
    @typic.al(strict = True)
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
            max(self.diff_hash()),
            max(self.diff_args()),
            max(self.diff_name()),
            max(self.diff_type()),
            max(self.diff_defs()),
            )

    @deal.pure
    @typic.al(strict = True)
    def diff_hash(self) -> numpy.ndarray:
        these = numpy.array([self.this] * self.size_max)
        those = numpy.array([self.that] * self.size_max)

        patch = [*self.patch, *self.filler(self.patch)]
        nones = [*self.nones, *self.filler(self.nones)]

        return numpy.where(these != those, patch, nones)

    @deal.pure
    @typic.al(strict = True)
    def diff_args(self) -> numpy.ndarray:
        these = numpy.array([self.this_len] * self.size_max)
        those = numpy.array([self.that_len] * self.size_max)

        major = [*self.major, *self.filler(self.major)]
        minor = [*self.minor, *self.filler(self.minor)]
        nones = [*self.nones, *self.filler(self.nones)]

        conds = [these < those, these > those, True]
        takes = [major, minor, nones]

        return numpy.select(conds, takes)

    @deal.pure
    @typic.al(strict = True)
    def diff_name(self) -> numpy.ndarray:
        these = numpy.array([a.name for a in self.this.arguments])
        those = numpy.array([a.name for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.major, self.nones]

        return [*numpy.select(conds, takes), *self.filler(self.minor)]

    @deal.pure
    @typic.al(strict = True)
    def diff_type(self) -> numpy.ndarray:
        these = numpy.array([a.types is None for a in self.this.arguments])
        those = numpy.array([a.types is None for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.patch, self.nones]

        return [*numpy.select(conds, takes), *self.filler(self.nones)]

    @deal.pure
    @typic.al(strict = True)
    def diff_defs(self) -> numpy.ndarray:
        major = [*self.major, *self.filler(self.major)]
        minor = [*self.minor, *self.filler(self.minor)]
        nones = [*self.nones, *self.filler(self.nones)]

        these = numpy.array(
            [a.default is None for a in self.this.arguments],
            int,
            )

        those = numpy.array(
            [a.default is None for a in self.that.arguments],
            int,
            )

        glued = tuple(zip(
            [*these, *[self.filler(self.nones), []][len(these) > len(those)]],
            [*those, *[self.filler(self.nones), []][len(those) > len(these)]],
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
