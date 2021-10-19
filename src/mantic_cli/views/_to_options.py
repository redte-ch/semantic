# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Parse task input to options.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import classes
import deal

from mantic import utils

from ..types import (
    OptionsAlias,
    TupleListAlias,
    TupleListType,
    TupleTupleAlias,
    TupleTupleType,
    )


@classes.typeclass
def to_options(instance) -> OptionsAlias:
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
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: tuple

        >>> to_options((*example1, *example2, *example3))
        (('-f --flag', 'How?', 'Like that!'), ('-f --flag', 'How?', 'Like ...))

    .. versionadded:: 1.0.0

    """

    ...  # pytype: disable=bad-return-type


@deal.pure
@to_options.instance(delegate = TupleListType)
def _from_tuple_list(instance: TupleListAlias) -> OptionsAlias:
    return tuple(utils.dcons(instance))


@deal.pure
@to_options.instance(delegate = TupleTupleType)
def _from_tuple_tuple(instance: TupleTupleAlias) -> OptionsAlias:
    return tuple(utils.dcons(instance))
