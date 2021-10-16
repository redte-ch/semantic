# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from typing import Any, Callable, MutableMapping, Sequence, Type, TypeVar

import deal
import toml
import typic

from pysemver import utils

T = TypeVar("T", bound = MutableMapping[str, Any])
F = TypeVar("F", bound = Callable[[str], T])


@typic.klass(frozen = True, slots = True, strict = True)
class Config:
    ignore: Sequence[str]


@deal.has("stdin")
@utils.pipes
def build_config(loader: F, config: Type[Config]) -> Config:
    return (
        "pyproject.toml"
        >> loader.load
        >> dict.get("tool")
        >> dict.get("pysemver")
        >> config.transmute
        )


config = build_config(toml, Config)
