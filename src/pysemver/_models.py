# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import typic
from aenum import Enum, IntEnum, skip


class Exit(IntEnum):
    """An enum with exit codes."""

    OK = 0
    KO = 1


@typic.klass(frozen = True, slots = True, strict = True)
class ArgType:
    """An argument type."""

    name: str


@typic.klass(frozen = True, slots = True, strict = True)
class RetType:
    """A return type."""

    name: str


@typic.klass(frozen = True, slots = True, strict = True)
class Argument:
    """An argument."""

    name: str
    types: Optional[Tuple[ArgType, ...]] = None
    default: Optional[str] = None


@typic.klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature, that is arguments and returns."""

    name: str
    file: str
    arguments: Sequence[Argument] = ()
    returns: Optional[Sequence[RetType]] = None


class Suffix(str, Enum):
    """An enum to find unique signature names."""

    SEMEL = ""
    BIS = "(bis)"
    TER = "(ter)"
    QUATER = "(quater)"
    QUINQUIES = "(quinquies)"
    SEXIES = "(sexies)"
    SEPTIES = "(septies)"
    OCTIES = "(octies)"
    NONIES = "(nonies)"
    DECIES = "(decies)"


class Version(Enum):

    @skip
    class Str(str, Enum):
        """An enum used to explain the required version.

        Examples:
            >>> [version.name for version in Version.Str]
            ['NONE', 'PATCH', 'MINOR', 'MAJOR']

            >>> [version.value for version in Version.Str]
            ['', '~', '+', '-']

        """

        NONE = ""
        PATCH = "~"
        MINOR = "+"
        MAJOR = "-"

    @skip
    class Int(IntEnum):
        """An enum used to determine the required version.

        Examples:
            >>> [version.name for version in Version.Int]
            ['NONE', 'PATCH', 'MINOR', 'MAJOR']

            >>> [version.value for version in Version.Int]
            [0, 1, 2, 3]

            >>> [str(version) for version in Version.Int]
            ['', '~', '+', '-']

        """

        NONE = 0
        PATCH = 1
        MINOR = 2
        MAJOR = 3

        @typic.al(strict = True)
        def __str__(self) -> str:
            return tuple(Version.Str)[self.value]
