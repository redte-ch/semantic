# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Configuration options.

For now, configuration options will be read from any valid ``pyproject.toml``
file.

For example::

    [tool.pysemver]
    exclude = [".editorconfig", ".gitignore", "tests"]

.. versionadded:: 1.0.0

"""

from typing import Any, Callable, MutableMapping, Sequence, Type, TypeVar

import deal
import toml
import typic

from pysemver import utils

T = TypeVar("T", bound = MutableMapping[str, Any])
F = TypeVar("F", bound = Callable[[str], T])


@typic.klass(frozen = True, slots = True, strict = True)
class Config:
    """Provides a configuration representation."""

    ignore: Sequence[str]


@deal.has("stdin")
@utils.pipes
def build_config(loader: F, config: Type[Config]) -> Config:
    """Builds the configuration."""

    return (
        "pyproject.toml"
        >> loader.load
        >> dict.get("tool")
        >> dict.get("pysemver")
        >> config.transmute
        )


config = build_config(toml, Config)
