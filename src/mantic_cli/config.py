# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Configuration options.

For now, configuration options will be read from any valid ``pyproject.toml``
or ``setup.cfg`` file.

For example::

    [tool.mantic]
    exclude = [".editorconfig", ".gitignore", "tests"]

.. versionchanged:: 1.2.0

.. versionadded:: 1.0.0

"""

from typing import Any, MutableMapping, Sequence, Type

from configparser import ConfigParser
from pathlib import Path

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

    from_file: MutableMapping[str, Any]

    if Path("pyproject.toml").exists():
        from_file = toml.load("pyproject.toml")
        return config.transmute(from_file["tool"]["mantic"])

    if Path("setup.cfg").exists():
        parser = ConfigParser()
        parser.read("setup.cfg")
        from_file = {"ignore": parser["tool:mantic"]["ignore"].split()}
        return config.transmute(from_file)

    raise NotImplementedError


config = build_config(Config)
