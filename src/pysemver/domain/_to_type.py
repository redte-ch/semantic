# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import classes


@classes.typeclass
def to_type(instance) -> str:
    """An argument/return type.

    Args:
        instance: Name of the type.

    Examples:
        >>> to_type("int")
        'int'

        >>> to_type(int)
        Traceback (most recent call last):
        NotImplementedError...

        >>> to_type(None)
        Traceback (most recent call last):
        NotImplementedError...

    .. versionadded:: 1.0.0

    """


@to_type.instance(str)
def _from_str(instance: str) -> str:
    return instance
