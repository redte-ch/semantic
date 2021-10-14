# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from typing import Any, Callable, MutableMapping, Sequence, Type, TypeVar

import pipeop
import toml

from . import typed

T = TypeVar("T", bound = MutableMapping[str, Any])
F = TypeVar("F", bound = Callable[[str], T])


@typed
class Config:
    ignore: Sequence[str]


@pipeop.pipes
def build_config(loader: F, config: Type[Config]) -> Config:
    return (
        "pyproject.toml"
        >> loader.load
        >> dict.get("tool")
        >> dict.get("pysemver")
        >> config.transmute
        )


config = build_config(toml, Config)
