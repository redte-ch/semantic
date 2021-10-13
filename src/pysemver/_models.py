# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import Any, Generic, MutableMapping, Sequence, TypeVar

import deal
import typic
from aenum import Enum, IntEnum, skip

T = TypeVar("T", bound = MutableMapping[str, Any])


@typic.klass(always = True, slots = True, strict = True)
class Config(Generic[T]):

    ignore: Sequence[str]


class Exit(IntEnum):
    """An enum with exit codes."""

    OK = 0
    KO = 1


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

        @deal.pure
        # @typic.al(strict = True)
        def __str__(self) -> str:
            return tuple(Version.Str)[self.value]
