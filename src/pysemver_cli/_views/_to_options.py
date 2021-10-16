# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import List, Tuple, Union

import classes
import deal

from pysemver import utils

OptionsType = Tuple[Tuple[str, str, str], ...]
TupleListType = List[Tuple[str, Tuple[str, str]]]
TupleTupleType = Tuple[Tuple[str, Tuple[str, str]], ...]


class _TupleListMeta(type):
    """Metaclass to check for a list of tuples."""

    def __instancecheck__(self, arg: object) -> bool:
        if not isinstance(arg, list):
            return False

        if not isinstance(arg[0], (list, tuple)):
            return False

        if not arg[0] or not isinstance(arg[0][0], str):
            return False

        return True


class _TupleTupleMeta(type):
    """Metaclass to check for a tuple of tuples."""

    def __instancecheck__(self, arg: object) -> bool:
        if not isinstance(arg, tuple):
            return False

        if not isinstance(arg[0], (list, tuple)):
            return False

        if not arg[0] or not isinstance(arg[0][0], str):
            return False

        return True


class _TupleList(List[tuple], metaclass = _TupleListMeta):
    """A list of tuples."""


class _TupleTuple(Tuple[tuple], metaclass = _TupleTupleMeta):
    """A tuple of tuples."""


@classes.typeclass
def to_options(instance) -> OptionsType:
    """A task's view content.

    Args:
        instance: Contents to parse.

    Examples:
        >>> example1 = ("-f --flag", ("How?", "Like that!")),
        >>> to_options(example1)
        (('-f --flag', 'How?', 'Like that!'),)

        >>> example2 = ["-f --flag", ("How?", "Like that!")],
        >>> to_options(example2)
        (('-f --flag', 'How?', 'Like that!'),)

        >>> example3 = [("-f --flag", ["How?", "Like that!"])]
        >>> to_options(example3)
        (('-f --flag', 'How?', 'Like that!'),)

        >>> example4 = "-f --flag", ("How?", "Like that!")
        >>> to_options(example4)
        (('-f --flag', 'How?', 'Like that!'),)

        >>> to_options(*example4)
        (('-f --flag', 'How?', 'Like that!'),)

        >>> to_options((*example1, *example2, *example3, example4))
        (('-f --flag', 'How?', 'Like that!'), ('-f --flag', 'How?', 'Like ...))

    .. versionadded:: 1.0.0

    """


@deal.pure
@to_options.instance(delegate = _TupleList)
def _from_tuple_list(instance: TupleListType) -> OptionsType:
    return tuple(utils.dcons(instance))


@deal.pure
@to_options.instance(delegate = _TupleTuple)
def _from_tuple_tuple(instance: TupleTupleType) -> OptionsType:
    return tuple(utils.dcons(instance))


@deal.pure
@to_options.instance(protocol = Tuple)
def _from_tuple(instance: Tuple[str, Tuple[str, str]]) -> OptionsType:
    return to_options([instance])


@deal.raises(NotImplementedError)
@deal.has()
@to_options.instance(str)
def _from_str(*instance: Union[str, Tuple[str, str]]) -> OptionsType:
    return to_options([instance])
