# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Optional, Tuple

import classes
import typic
from returns import pipeline

from .. import _fn
from ._arg_type import arg_types
from ._default import default


@typic.klass(frozen = True, slots = True, strict = True)
class ArgSchema:
    """An argument.

    Attributes:
        name: The name of the attribute
        types: The types of the attribute, if any.
        default: The defaul value of the attribute, if any.

    Examples:
        >>> _Arg("count", ("int",), "1")
        _Arg(name='count', types=('int',), default='1')

        >>> _Arg("count", None, None)
        _Arg(name='count', types=None, default=None)

        >>> _Arg("count", int, 1)
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

    . versionadded:: 1.0.0

    """

    name: str
    types: Optional[Tuple[str, ...]]
    default: Optional[str]


@classes.typeclass
def arg(instance) -> Tuple[str, arg_types, default]:
    """An argument.

    Args:
        instance: A tuple (name, types, default).

    Examples:
        >>> arg("count")
        ('count', None, None)

        >>> arg("count", None)
        ('count', None, None)

        >>> arg(None)
        None

        >>> arg(1)
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: int

    . versionadded:: 1.0.0

    """


@arg.instance(str)
def _arg(instance: str) -> Tuple[str, arg_types, default]:
    return tuple(map(_fn.second, ArgSchema(instance, None, None)))
