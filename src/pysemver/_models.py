from __future__ import annotations

from typing import Optional, Sequence, Tuple

import typic
from aenum import Enum, IntEnum, skip
from typic import klass


@klass(frozen = True, slots = True, strict = True)
class ArgType:
    """An argument type."""

    name: str


@klass(frozen = True, slots = True, strict = True)
class RetType:
    """A return type."""

    name: str


@klass(frozen = True, slots = True, strict = True)
class Argument:
    """An argument."""

    name: str
    types: Optional[Tuple[ArgType, ...]] = None
    default: Optional[str] = None


@klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature, that is arguments and returns."""

    name: str
    file: str
    arguments: Sequence[Argument] = ()
    returns: Optional[Sequence[RetType]] = None


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
