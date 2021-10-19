# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Argument schema.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Any, Optional

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
        Argument(name='count', default=None)

        >>> Argument("count", "None")
        Argument(name='count', default='None')

        >>> Argument("count", "1")
        Argument(name='count', default='1')

        >>> Argument("count", 1)
        Argument(name='count', default=1)

    .. versionadded:: 1.0.0

    """

    name: str
    default: Optional[Any] = None
