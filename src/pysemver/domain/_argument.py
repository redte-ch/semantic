# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Optional, Tuple

import typic


@typic.klass(frozen = True, slots = True, strict = True)
class Argument:
    """An argument.

    Attributes:
        name: The name of the argument.
        types: The annotations, if any.
        default: The default value, if any.

    Examples:
        >>> Argument("count")
        Argument(name='count', types=None, default=None)

        >>> Argument("count", ("int",))
        Argument(name='count', types=('int',), default=None)

        >>> Argument("count", "int")
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

        >>> Argument("count", int)
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

        >>> Argument("count", ("int",), "None")
        Argument(name='count', types=('int',), default='None')

        >>> Argument("count", ("int",), "1")
        Argument(name='count', types=('int',), default='1')

        >>> Argument("count", ("int",), 1)
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

    .. versionadded:: 1.0.0

    """

    name: str
    types: Optional[Tuple[str, ...]] = None
    default: Optional[str] = None
