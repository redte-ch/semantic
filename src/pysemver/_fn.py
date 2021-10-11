# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

"""Somme handy functions to parse data."""

import functools
import itertools
from typing import Any, Callable, Sequence, TypeVar

import deal

T = TypeVar("T")
F = Callable[..., Any]

partial = functools.partial


@deal.pure
def apply(func: F, seqs: Any) -> Any:
    """Applies a function to a sequence of sequences.

    Args:
        func: Any callable.
        sequences: Any sequence of sequences.

    Examples:
        >>> func = lambda *x: sum(x)
        >>> list(apply(func, [(1, 2), (3, 4)]))
        [3, 7]

    """

    return (func(*seq) for seq in seqs)


@deal.pure
def cons(seqs: Any) -> Any:
    """Like the original cons but for sequences of sequences.

        Args:
            seqs: Infinite sequences of infinite sequences.

        Examples:
            >>> list(cons([(1, [2, 3]), (4, [5, 6]), (7, [8, 9])]))
            [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

    """

    return (tuple(itertools.chain([el], seq)) for el, seq in seqs)


@deal.pure
def first(seq: Sequence[T]) -> T:
    """Returns the first element of a sequence.

    Args:
        seq: Any sequence.

    Examples:
        >>> first([1, 2, 3])
        1

    """

    return next(iter(seq))
