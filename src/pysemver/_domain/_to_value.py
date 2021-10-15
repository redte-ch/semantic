# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import ast

import classes


@classes.typeclass
def to_value(instance) -> str:
    """An ast node to it's value in str.

    Args:
        instance: Type of the node.

    Examples:
        >>> to_value(ast.Attribute(attr = "hey!"))
        'hey!'

        >>> to_value(ast.Call(func = "hey!"))
        'hey!'

        >>> to_value(ast.Constant(value = "hey!"))
        'hey!'

        >>> to_value(ast.Ellipsis())
        '...'

        >>> to_value(ast.Name(id = "hey!"))
        'hey!'

        >>> to_value(ast.NameConstant(value = "hey!"))
        'hey!'

        >>> to_value(ast.Num(n = "hey!"))
        'hey!'

        >>> to_value(ast.Str(s = "hey!"))
        'hey!'

    .. versionadded:: 1.0.0

    """


@to_value.instance(ast.Attribute)
def _from_ast_attribute(instance: ast.Attribute) -> str:
    return to_value(instance.attr)


@to_value.instance(ast.Call)
def _from_ast_call(instance: ast.Call) -> str:
    return to_value(instance.func)


@to_value.instance(ast.Constant)
def _from_ast_constant(instance: ast.Constant) -> str:
    return to_value(instance.value)


@to_value.instance(type(Ellipsis))
def _from_ast_ellipsis(instance: ast.Ellipsis) -> str:
    return "..."


@to_value.instance(ast.Name)
def _from_ast_name(instance: ast.Name) -> str:
    return to_value(instance.id)


@to_value.instance(ast.NameConstant)
def _from_ast_name_constant(instance: ast.NameConstant) -> str:
    return to_value(instance.value)


@to_value.instance(ast.Num)
def _from_ast_num(instance: ast.Num) -> str:
    return to_value(instance.n)


@to_value.instance(ast.Str)
def _from_ast_str(instance: ast.Str) -> str:
    return to_value(instance.s)


@to_value.instance(str)
def _from_str(instance: str) -> str:
    return instance
