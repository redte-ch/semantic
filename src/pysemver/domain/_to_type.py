# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import ast

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


@to_type.instance(ast.Constant)
def _from_ast_constant(instance: ast.Constant) -> str:
    return to_type(instance.value)


@to_type.instance(ast.Name)
def _from_ast_name(instance: ast.Name) -> str:
    return to_type(instance.id)


@to_type.instance(ast.Subscript)
def _from_ast_subscript(instance: ast.Subscript) -> str:
    return (to_type(instance.value), to_type(instance.slice))


@to_type.instance(str)
def _from_str(instance: str) -> str:
    return instance


@to_type.instance(None)
def _from_none(instance: None) -> None:
    return instance
