# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import classes


@classes.typeclass
def type_annotation(instance) -> str:
    """An argument/return type.

    Args:
        instance: Name of the type.

    Examples:
        >>> type_annotation("int")
        'int'

        >>> type_annotation(int)
        Traceback (most recent call last):
        NotImplementedError...

        >>> type_annotation(None)
        Traceback (most recent call last):
        NotImplementedError...

    . versionadded:: 1.0.0

    """


@type_annotation.instance(str)
def _type_str(instance: str) -> str:
    return instance
