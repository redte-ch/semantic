# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Configuration options.

For now, configuration options will be read from any valid ``pyproject.toml``
file.

For example::

    [tool.mantic]
    exclude = [".editorconfig", ".gitignore", "tests"]

.. versionadded:: 1.0.0

"""

from typing import Any, MutableMapping, Sequence, Type

import deal
import toml
import typic


@typic.klass(frozen = True, slots = True, strict = True)
class Config:
    """Provides a configuration representation."""

    ignore: Sequence[str]


@deal.has("import")
def build_config(config: Type[Config]) -> Config:
    """Builds the configuration."""

    from_toml: MutableMapping[str, Any] = toml.load("pyproject.toml")

    return config.transmute(from_toml["tool"]["mantic"])


config = build_config(Config)
