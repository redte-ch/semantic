# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Any, Tuple, Union

import typic

from ._argument import Argument


@typic.klass(frozen = True, slots = True)
class Signature:
    """A signature.

    Attributes:
        name: The name of the function.
        file: The file where the function is defined.
        arguments: All the :class:`.Argument` of the function.
        returns: The return values, if any.

    Examples:
        >>> Signature("greet", "file.py")
        Signature(name='greet', file='file.py', arguments=(), returns=None)

        >>> argument = Argument("count", ("int",), "1")

        >>> Signature("greet", "file.py", argument)
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

        >>> Signature("greet", "file.py", (argument,))
        Signature(name='greet', file='file.py', arguments=(Argument(name='co...

        >>> Signature("greet", "file.py", (), ("None",))
        Signature(name='greet', file='file.py', arguments=(), returns=('None...

        >>> Signature("greet", "file.py", (), None)
        Signature(name='greet', file='file.py', arguments=(), returns=None)

        >>> Signature("greet", "file.py", (), "int")
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

        >>> Signature("greet", "file.py", (), [int])
        Traceback (most recent call last):
        typic.constraints.error.ConstraintValueError...

    .. versionadded:: 1.0.0

    """

    name: str
    file: str
    arguments: Tuple[Argument] = ()
    returns: Union[str, Tuple[str, Tuple[Any]]] = None

    def __len__(self) -> int:
        return len(self.arguments)
