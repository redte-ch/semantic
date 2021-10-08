import dataclasses
import enum
from typing import Optional

import numpy

from ._builder import Contract


class SemVer(enum.Enum):
    """An enum just to express a release.

    Examples:
        >>> [version.name for version in SemVer]
        ['NONES', 'PATCH', 'MINOR', 'MAJOR']

        >>> [version.value for version in SemVer]
        ['nones', 'patch', 'minor', 'major']

        >>> [version.index for version in SemVer]
        [0, 1, 2, 3]

    """

    NONES = 0
    PATCH = 1
    MINOR = 2
    MAJOR = 3


@dataclasses.dataclass
class FuncChecker:

    this: Contract
    that: Contract
    reason: Optional[str] = None

    def __post_init__(self):
        self.this_len: int = len(self.this.arguments)
        self.that_len: int = len(self.that.arguments)
        self.this_add: int = max(self.that_len - self.this_len, 0)
        self.that_add: int = max(self.this_len - self.that_len, 0)
        self.size_max: int = max(self.this_len, self.that_len)
        self.size_min: int = min(self.this_len, self.that_len)

    @property
    def nones(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.NONES.value, self.size_min)

    @property
    def patch(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.PATCH.value, self.size_min)

    @property
    def minor(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.MINOR.value, self.size_min)

    @property
    def major(self) -> numpy.ndarray:
        return numpy.repeat(SemVer.MAJOR.value, self.size_min)

    def filler(self, array: numpy.ndarray) -> numpy.ndarray:
        index: int = array[0]
        times: int = max(self.this_add, self.that_add)

        return numpy.repeat(index, times)

    def function(self) -> None:
        return None

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

    def diff_hash(self) -> numpy.ndarray:
        these = numpy.array([self.this] * self.size_max)
        those = numpy.array([self.that] * self.size_max)

        patch = [*self.patch, *self.filler(self.patch)]
        nones = [*self.nones, *self.filler(self.nones)]

        return numpy.where(these != those, patch, nones)

    def diff_args(self) -> numpy.ndarray:
        these = numpy.array([self.this_len] * self.size_max)
        those = numpy.array([self.that_len] * self.size_max)

        major = [*self.major, *self.filler(self.major)]
        minor = [*self.minor, *self.filler(self.minor)]
        nones = [*self.nones, *self.filler(self.nones)]

        conds = [these < those, these > those, True]
        takes = [major, minor, nones]

        return numpy.select(conds, takes)

    def diff_name(self) -> numpy.ndarray:
        these = numpy.array([a.name for a in self.this.arguments])
        those = numpy.array([a.name for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.major, self.nones]

        return [*numpy.select(conds, takes), *self.filler(self.minor)]

    def diff_type(self) -> numpy.ndarray:
        these = numpy.array([a.types is None for a in self.this.arguments])
        those = numpy.array([a.types is None for a in self.that.arguments])
        glued = tuple(zip(these, those))

        conds = [[this != that for this, that in glued], True]
        takes = [self.patch, self.nones]

        return [*numpy.select(conds, takes), *self.filler(self.nones)]

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
