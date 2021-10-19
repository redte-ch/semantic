# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Exit schema.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from enum import IntEnum


class Exit(IntEnum):
    """An enum with exit codes.

    Examples:
        >>> [exit for exit in Exit]
        [<Exit.OK: 0>, <Exit.KO: 1>]

    .. versionadded:: 1.0.0

    """

    OK = 0
    KO = 1
