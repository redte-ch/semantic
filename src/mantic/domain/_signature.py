# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Signature schema.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Tuple

import typic

from ._argument import Argument


@typic.klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature.

    Attributes:
        name: The name of the function.
        file: The file where the function is defined.
        arguments: All the :class:`.Argument` of the function.
        returns: The return values, if any.

    Examples:
        >>> Signature("greet", "file.py")
        Signature(name='greet', file='file.py', arguments=())

        >>> argument = Argument("count", "1")

        >>> Signature("greet", "file.py", argument)
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

        >>> Signature("greet", "file.py", (argument,))
        Signature(name='greet', file='file.py', arguments=(Argument(name='co...

    .. versionadded:: 1.0.0

    """

    name: str
    file: str
    arguments: Tuple[Argument, ...] = ()

    def __len__(self) -> int:
        return len(self.arguments)
