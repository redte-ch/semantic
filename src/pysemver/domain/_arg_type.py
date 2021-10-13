# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Optional, Tuple

import classes

from .._types import StringTuple


@classes.typeclass
def arg_type(instance) -> str:
    """An argument type.

    Args:
        instance: Name of the type.

    Examples:
        >>> arg_type("int")
        'int'

        >>> arg_type(int)
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: type

    . versionadded:: 1.0.0

    """


@arg_type.instance(str)
def _arg_type(instance: str) -> str:
    return instance


@classes.typeclass
def arg_types(instance) -> Optional[Tuple[arg_type]]:
    """Argument types.

    Args:
        names: A sequence with the type names.

    Examples:
        >>> arg_types(("List", "int"))
        ('List', 'int')

        >>> arg_types(*["List", "int"])
        ('List', 'int')

        >>> arg_types((arg_type("int")))
        ('int',)

        >>> arg_types(None)
        None

        >>> arg_types(["int"])
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: list

        >>> arg_types({"List", "int"})
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: set

        >>> arg_types(("List", int))
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: tuple

    . versionadded:: 1.0.0

    """


@arg_types.instance(delegate = StringTuple)
def _arg_types_tuple(instance: Tuple[str]) -> Tuple[str]:
    return instance


@arg_types.instance(None)
def _arg_types_none(instance: None) -> None:
    return instance


@arg_types.instance(str)
def _arg_types_str(*instance: str) -> Tuple[str]:
    return tuple(instance)
