# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Version schema."""

from __future__ import annotations

from enum import Enum, IntEnum


class VersionStr(str, Enum):
    """An enum used to explain the required version.

    Examples:
        >>> [version.name for version in VersionStr]
        ['NONE', 'PATCH', 'MINOR', 'MAJOR']

        >>> [version.value for version in VersionStr]
        ['', '~', '+', '-']

    """

    NONE = ""
    PATCH = "~"
    MINOR = "+"
    MAJOR = "-"


class VersionInt(IntEnum):
    """An enum used to determine the required version.

    Examples:
        >>> [version.name for version in VersionInt]
        ['NONE', 'PATCH', 'MINOR', 'MAJOR']

        >>> [version.value for version in VersionInt]
        [0, 1, 2, 3]

        >>> [str(version) for version in VersionInt]
        ['', '~', '+', '-']

    """

    NONE = 0
    PATCH = 1
    MINOR = 2
    MAJOR = 3

    def __str__(self) -> str:
        return tuple(VersionStr)[self.value]
