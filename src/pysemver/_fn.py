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

import itertools
from typing import (
    Callable,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    )

import deal
import returns.curry

T = TypeVar("T")

chain = itertools.chain
"""Just a shortcut for `.itertools.chain`."""

partial = returns.curry.partial
"""Just a shortcut for `.functools.partial`."""


@deal.pure
def _(x: T) -> Callable[..., T]:
    """Identity useful for noop.

    Examples:
        >>> _(1)()
        1

    .. versionadded:: 1.0.0

    """

    return lambda: x


@deal.ensure(lambda func, result: func.args[0] == result)
@deal.raises(NotImplementedError)
@deal.has()
def do(func: Callable[..., T]) -> T:
    """Do something on something, thent return something.

    Args:
        func: Something.

    Returns:
        Any: The original thing.

    Examples:
        >>> x = "hey!"
        >>> func = partial(str.upper, x)
        >>> func()
        >>> do(func)
        'hey!'

    Todo:
        Fix types.

    .. versionadded:: 1.0.0

    """

    if not hasattr(func, "args"):
        raise NotImplementedError

    if not hasattr(func, "keywords"):
        raise NotImplementedError

    self, *args = func.args  # type: ignore

    func.func(self, *args, **func.keywords)  # type: ignore

    return self


@deal.pure
def dfc(seqs: Sequence[Tuple[T, Iterable[T]]]) -> Iterator[Tuple[T, ...]]:
    """Like the original cons but for cons of cons.

    Args:
        seqs: Any sequences of sequences.

    Examples:
        >>> list(dfc[(1, [2, 3]), (4, [5, 6])]))
        [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

    .. versionadded:: 1.0.0

    """

    return (tuple(itertools.chain([el], seq)) for el, seq in seqs)


@deal.pure
def dfp(func: Callable[[T], T], seqs: Sequence[Sequence[T]]) -> Iterator[T]:
    """Applies a function to a sequence of sequences.

    Args:
        func: Any callable.
        seqs: Any sequence of sequences.

    Examples:
        >>> list(dfp(float.__add__, [(.1, .2), (.3, .4)]))
        [0.3..., 0.7]

    .. versionadded:: 1.0.0

    """

    return (func(*seq) for seq in seqs)


@deal.pure
def first(seq: Sequence[T]) -> Optional[T]:
    """Returns the first element of a sequence.

    Args:
        seq: Any sequence.

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

    Examples:
        >>> list(compact(["1", 0, "a", None, {}]))
        ['1', 'a']

    .. versionadded:: 1.0.0

    """

    return filter(bool, seq)


@deal.ensure(lambda seqs, result: seqs[0][0] is list(result)[0])
@deal.raises(NotImplementedError)
@deal.has()
def flatten(seqs: Sequence[Sequence[T]]) -> Iterator[T]:
    """Flattens a sequences of sequences.

    Args:
        seqs: Any sequence of sequences.

    Examples:
        >>> list(flatten([(1, 2), (3, 4)]))
        [1, 2, 3, 4]

        >>> list(flatten(["ab", "cd"]))
        ['a', 'b', 'c', 'd']

    .. versionadded:: 1.0.0

    """

    if len(seqs) < 1:
        raise NotImplementedError

    if any(map(lambda x: len(x) < 1, seqs)):
        raise NotImplementedError

    return chain.from_iterable(seqs)
