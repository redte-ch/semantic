from __future__ import annotations

import abc
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
