# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Any

import sys

if sys.version_info >= (3, 8):
    from typing import Literal

else:
    from typing_extensions import Literal


What = Literal["this", "that"]


# TODO: fix this (move to pysemver_hypothesis)
class PartialLike:

    def __init__(self) -> None:
        self.func = self
        self.args = sum, *(1, 2, 3)
        self.keywords = {"a": 1, "b": 2, "c": 3}

    def __call__(self, *args: Any, **kwds: Any) -> None:
        ...
