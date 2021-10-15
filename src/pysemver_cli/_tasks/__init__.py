# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import MutableMapping, Sequence, Tuple

import sys

import invoke
import pipeop
import typic
from invoke import Collection

from pysemver import actions, infra
# TODO: remove this
from pysemver._types import HasExit

from .._config import config


@typic.klass(always = True, slots = True, strict = True)
class CheckVersionTask:

    optional: Sequence[str]
    help: MutableMapping[str, Tuple[str, ...]]

    @pipeop.pipes
    def __init__(self, ignore: Sequence[str]) -> None:
        self.optional = ["ignore"]
        self.help = {
            "ignore": (
                "Paths to ignore",
                f"{ignore << str.join(', ')}"
                ),
            }


class Tasks(Collection):

    def __init__(self) -> None:
        super().__init__()
        self.add_task(self.check_deprecated)
        self.add_task(self.check_version)

    @invoke.task
    def check_deprecated(_context):
        """Check if there are features to deprecate."""

        task: HasExit
        task = actions.CheckDeprecated(infra.logger)
        task()
        sys.exit(task.exit.value)

    @invoke.task(**CheckVersionTask(config.ignore).primitive())
    def check_version(_context, ignore = config.ignore):
        """Check if the actual version is valid."""

        task: HasExit
        task = actions.CheckVersion(infra.logger)
        task()
        sys.exit(task.exit.value)
