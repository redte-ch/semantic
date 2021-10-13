# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Optional, Tuple

import classes

from .._types import StringTuple


@classes.typeclass
def ret_type(instance) -> str:
    """A return type.

    Args:
        instance: Name of the type.

    Examples:
        >>> ret_type("int")
        'int'

        >>> ret_type(int)
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: type

    . versionadded:: 1.0.0

    """


@ret_type.instance(str)
def _ret_type(instance: str) -> str:
    return instance


@classes.typeclass
def ret_types(instance) -> Optional[Tuple[str]]:
    """Return types.

    Args:
        names: A sequence with the type names.

    Examples:
        >>> ret_types(("List", "int"))
        ('List', 'int')

        >>> ret_types(*["List", "int"])
        ('List', 'int')

        >>> ret_types((ret_type("int")))
        ('int',)

        >>> ret_types(None)
        None

        >>> ret_types(["int"])
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: list

        >>> ret_types({"List", "int"})
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: set

        >>> ret_types(("List", int))
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: tuple

    . versionadded:: 1.0.0

    """


@ret_types.instance(delegate = StringTuple)
def _ret_types_tuple(instance: Tuple[str]) -> Tuple[str]:
    return instance


@ret_types.instance(None)
def _ret_types_none(instance: None) -> None:
    return instance


@ret_types.instance(str)
def _ret_types_str(*instance: str) -> Tuple[str]:
    return tuple(instance)
