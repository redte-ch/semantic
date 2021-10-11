# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

import functools
from typing import Sequence, TypeVar

import deal
import typic

T = TypeVar("T")

partial = functools.partial


def _(x):
    return x


@deal.pure
def first(sequence: Sequence[T]) -> T:
    """Returns the first element of a sequence.

    Args:
        sequence: Any sequence.

    Examples:
        >>> first([1,2,3])
        1

    """

    return next(iter(sequence))
