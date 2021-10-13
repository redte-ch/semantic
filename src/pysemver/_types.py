# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import Optional, Tuple

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


ArgName = str
ArgDefault = Optional[str]
ArgTypeAnn = Optional[Tuple[str, ...]]
