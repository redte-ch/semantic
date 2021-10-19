# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Common types.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import List, Tuple

OptionsAlias = Tuple[Tuple[str, ...], ...]
TupleListAlias = List[Tuple[str, Tuple[str, str]]]
TupleTupleAlias = Tuple[Tuple[str, Tuple[str, str]], ...]


class _TupleListMeta(type):
    """Metaclass to check for a list of tuples."""

    def __instancecheck__(cls, arg: object) -> bool:
        if not isinstance(arg, list):
            return False

        elif not arg[0] or not isinstance(arg[0], (list, tuple)):
            return False

        elif not arg[0][0] or not isinstance(arg[0][0], str):
            return False

        return True


class _TupleTupleMeta(type):
    """Metaclass to check for a tuple of tuples."""

    def __instancecheck__(cls, arg: object) -> bool:
        if not isinstance(arg, tuple):
            return False

        elif not arg[0] or not isinstance(arg[0], (list, tuple)):
            return False

        elif not arg[0][0] or not isinstance(arg[0][0], str):
            return False

        return True


class TupleListType(TupleListAlias, metaclass = _TupleListMeta):
    """A list of tuples."""


class TupleTupleType(TupleTupleAlias, metaclass = _TupleTupleMeta):
    """A tuple of tuples."""
