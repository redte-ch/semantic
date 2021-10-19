# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Suffix schema.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from enum import Enum


class Suffix(str, Enum):
    """An enum to find unique signature names.

    Examples:
        >>> Suffix.BIS
        <Suffix.BIS: '(bis)'>

    .. versionadded:: 1.0.0

    """

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
