# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Handy numpy generators.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import deal
import numpy

import mantic_hypothesis as st

from ..domain import Signature

st.register(Signature, st.signatures)

size_limit = 2e5
"""Just a random size/length sentinel."""

what_limit = 2e20
"""Just a random size/length sentinel."""

limit_bound = deal.chain(
    deal.pre(lambda _: size_limit > _.this >= 0),
    deal.pre(lambda _: size_limit > _.that >= 0),
    deal.pre(lambda _: what_limit > _.what >= 0),
    )
"""Bind these values to some arbitrary limit."""


@deal.pre(lambda this, that: this >= 0 and that >= 0)
@deal.pure
def add(this: int, that: int) -> int:
    """Calculates the offset between two numbers.

    Args:
        this: An upper/lower bound value.
        that: Another upper/lower bound value.

    Returns:
        int: The value.

    Examples:
        >>> add(1, 2)
        1

        >>> add(2, 1)
        0

        >>> add(0, 0)
        0

    .. versionadded:: 1.0.0

    """

    return max(that - this, 0)


@limit_bound
@deal.pure
def pre(this: int, that: int, what: int) -> numpy.ndarray:
    """Pre-populates a numpy array.

    Args:
        this: An upper/lower bound value.
        that: Another upper/lower bound value.
        what: What to pre-populate the array with.

    Returns:
        numpy.ndarray: The pre-populated array.

    Examples:
        >>> pre(10, 5, 1)
        array([1, 1, 1, 1, 1])

    .. versionadded:: 1.0.0

    """

    return numpy.repeat(what, min(this, that))


@limit_bound
@deal.pure
def rep(this: int, that: int, what: int) -> numpy.ndarray:
    """Repeats a value over a numpy array.

    Args:
        this: An upper/lower bound value.
        that: Another upper/lower bound value.
        what: What to repeat over the array with.

    Returns:
        numpy.ndarray: The repeated array.

    Examples:
        >>> rep(10, 5, 1)
        array([1, 1, 1, 1, 1])

    .. versionadded:: 1.0.0

    """

    return numpy.repeat(abs(what), max(add(this, that), add(that, this)))


@limit_bound
@deal.pure
def pop(this: int, that: int, what: int) -> numpy.ndarray:
    """Pre-populates & repeats a value over a numpy array.

    Args:
        this: An upper/lower bound value.
        that: Another upper/lower bound value.
        what: What to populate the array with.

    Returns:
        numpy.ndarray: The populated array.

    Examples:
        >>> pop(10, 5, 1)
        array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    .. versionadded:: 1.0.0

    """

    return numpy.array([*pre(this, that, what), *rep(this, that, what)])


@limit_bound
@deal.pure
def fill(this: int, that: int, what: int) -> numpy.ndarray:
    """Fill a numpy array with anything.

    Args:
        this: An upper/lower bound value.
        that: Another upper/lower bound value.
        what: What to fill the array with.

    Returns:
        numpy.ndarray: The filled array.

    Examples:
        >>> fill(1, 2, 3)
        array([3, 3])

    .. versionadded:: 1.0.0

    """

    return numpy.array([what] * max(this, that))
