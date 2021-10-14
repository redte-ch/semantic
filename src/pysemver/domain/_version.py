# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import aenum
from aenum import Enum, IntEnum


class Version(Enum):

    @aenum.skip
    class Str(str, Enum):
        """An enum used to explain the required version.

        Examples:
            >>> [version.name for version in Version.Str]
            ['NONE', 'PATCH', 'MINOR', 'MAJOR']

            >>> [version for version in Version.Str]
            ['', '~', '+', '-']

        """

        NONE = ""
        PATCH = "~"
        MINOR = "+"
        MAJOR = "-"

    @aenum.skip
    class Int(IntEnum):
        """An enum used to determine the required version.

        Examples:
            >>> [version.name for version in Version.Int]
            ['NONE', 'PATCH', 'MINOR', 'MAJOR']

            >>> [version for version in Version.Int]
            [0, 1, 2, 3]

            >>> [str(version) for version in Version.Int]
            ['', '~', '+', '-']

        """

        NONE = 0
        PATCH = 1
        MINOR = 2
        MAJOR = 3

        def __str__(self) -> str:
            return tuple(Version.Str)[self.value]
