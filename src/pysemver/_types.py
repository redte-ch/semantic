# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import Any, Callable, Tuple

import abc
import sys

import pipeop
from phantom import Phantom
from phantom.predicates import collection, generic

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol

else:
    from typing_extensions import Literal, Protocol


@pipeop.pipes
def _type(value: type) -> Callable[..., Any]:
    return (
        value
        >> generic.of_type
        >> collection.every
        )


What = Literal["this", "that"]


class HasIndex(Protocol):
    index: int


class HasExit(Protocol):
    exit: HasIndex

    @abc.abstractmethod
    def __call__(self) -> None:
        ...


class StringTuple(Tuple[str], Phantom, predicate = _type(str)):
    ...
