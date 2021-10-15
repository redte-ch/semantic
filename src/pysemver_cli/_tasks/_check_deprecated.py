# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import sys

import invoke

from pysemver import actions, infra

from .._config import config
from ._task import Task

task = Task.transmute({
    "optional": ("ignore",),
    "help": {
        "ignore": (
            "Paths to ignore",
            f"{', '.join(config.ignore)}",
            ),
        },
    })


@invoke.task(**task.primitive())
def check_deprecated(_context, ignore = config.ignore):
    """Check if there are features to deprecate."""

    task = actions.CheckDeprecated(infra.logger)
    task()
    sys.exit(task.exit.value)
