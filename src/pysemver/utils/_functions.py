# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Somme handy functions to pipe data.

These are rather convenient for building the interface, and traversing the
AST and so on…

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    )

import itertools

import deal
import returns.curry

T = TypeVar("T")

chain = itertools.chain
"""Just a shortcut for `.itertools.chain`."""

partial = returns.curry.partial
"""Just a shortcut for `.functools.partial`."""


@deal.pure
def cons(el: T, seq: Iterable[T]) -> Iterator[T]:
    """The original cons.

    Args:
        el: An element.
        seq: Any sequence.

    Returns:
        An iterator with the values.


    Examples:
        >>> list(cons(1, (2, 3)))
        [1, 2, 3]

    .. versionadded:: 1.0.0

    """

    return itertools.chain([el], seq)


@deal.pure
def dcons(seqs: Sequence[Tuple[T, Iterable[T]]]) -> Iterator[Tuple[T, ...]]:
    """Like the original cons but for cons of cons.

    Args:
        seqs: Any sequences of sequences.

    Returns:
        An iterator with the values.

    Examples:
        >>> list(dcons([(1, [2, 3]), (4, [5, 6])]))
        [(1, 2, 3), (4, 5, 6)]

    .. versionadded:: 1.0.0

    """

    return (tuple(cons(el, seq)) for el, seq in seqs)


def dmap(func: Callable[[T], Any], seqs: Sequence[Sequence[T]]) -> Iterator[T]:
    """Applies a function to a sequence of sequences.

    Args:
        func: Any callable.
        seqs: Any sequence of sequences.

    Returns:
        An iterator with the values.

    Examples:
        >>> list(dmap(float.__add__, [(.1, .2), (.3, .4)]))
        [0.3..., 0.7]

    .. versionadded:: 1.0.0

    """

    return (func(*seq) for seq in seqs)


@deal.pure
def first(seq: Sequence[T]) -> Optional[T]:
    """Returns the first element of a sequence.

    Args:
        seq: Any sequence.

    Returns:
        The first value, or None.

    Examples:
        >>> first([1, 2, 3])
        1

        >>> first([])
        None

    .. versionadded:: 1.0.0

    """

    return next(iter(seq), None)


@deal.pure
def compact(seq: Iterable[T]) -> Iterator[T]:
    """ Filters falsy values.

    Args:
        seq: Any sequence.

    Returns:
        An iterator with the values.

    Examples:
        >>> list(compact(["1", 0, "a", None, {}]))
        ['1', 'a']

    .. versionadded:: 1.0.0

    """

    return filter(bool, seq)


@deal.pre(lambda seqs: any(map(lambda x: len(x) > 0, seqs)))
@deal.pre(lambda seqs: len(seqs) > 0)
@deal.pure
def flatten(seqs: Sequence[Sequence[T]]) -> Iterator[T]:
    """Flattens a sequences of sequences.

    Args:
        seqs: Any sequence of sequences.

    Returns:
        An iterator with the values.

    Examples:
        >>> list(flatten([(1, 2), (3, 4)]))
        [1, 2, 3, 4]

        >>> list(flatten(["ab", "cd"]))
        ['a', 'b', 'c', 'd']

    .. versionadded:: 1.0.0

    """

    return chain.from_iterable(seqs)
