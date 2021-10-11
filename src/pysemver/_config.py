# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from typing import Any, Callable, MutableMapping, Type, TypeVar

import toml
from lambdas import _
from pipeop import pipes

from ._models import Config

T = TypeVar("T", bound = MutableMapping[str, Any])
F = TypeVar("F", bound = Callable[[str], T])


@pipes
def build_config(loader: F, config: Type[Config]) -> Config[T]:
    return (
        "pyproject.toml"
        >> loader.load
        >> _["tool"]
        >> _["pysemver"]
        >> config.transmute
        )


config = build_config(toml, Config)
