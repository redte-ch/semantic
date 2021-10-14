# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import Any

import abc
import dataclasses
import sys

if sys.version_info >= (3, 8):
    from typing import Literal, Protocol

else:
    from typing_extensions import Literal, Protocol


What = Literal["this", "that"]


class HasIndex(Protocol):
    index: int


class HasExit(Protocol):
    exit: HasIndex

    @abc.abstractmethod
    def __call__(self) -> None:
        ...


@dataclasses.dataclass
class DataclassLike(abc.ABC):
    some: str
    thing: str


class PartialLike:

    def __init__(self) -> None:
        self.func = self
        self.args = sum, *(1, 2, 3)
        self.keywords = {"a": 1, "b": 2, "c": 3}

    def __call__(self, *args: Any, **kwds: Any) -> None:
        ...
