# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

import sys
from typing import MutableMapping, Sequence, Tuple

import invoke
import pipeop
import typic
from invoke import Collection

from ._check_deprecated import CheckDeprecated
from ._check_version import CheckVersion
from ._config import config
from ._types import HasExit
from ._bar import Bar


@typic.klass(always = True, slots = True, strict = True)
class CheckVersionTask:

    optional: Sequence[str]
    help: MutableMapping[str, Tuple[str, ...]]

    @pipeop.pipes
    def __init__(self, ignore: Sequence[str]) -> None:
        self.optional = ["ignore"]
        self.help = {
            "pico": (
                "Paths to ignore",
                f"default: {ignore << str.join(', ')}"),
            "ignore": (
                "Paths to ignore",
                f"(default: {ignore << str.join(', ')}"),
            }


class Tasks(Collection):

    bar = Bar()

    def __init__(self) -> None:
        super().__init__()
        self.add_task(self.check_deprecated)
        self.add_task(self.check_version)

    @invoke.task
    def check_deprecated(_context):
        """Check if there are features to deprecate."""

        task: HasExit
        task = CheckDeprecated(Tasks.bar)
        task()
        sys.exit(task.exit.value)

    @invoke.task(**CheckVersionTask(config.ignore).primitive())
    def check_version(_context, pico, pichula, ignore = config.ignore):
        """Check if the actual version is valid."""

        # breakpoint()
        task: HasExit
        task = CheckVersion(Tasks.bar)
        task()
        sys.exit(task.exit.value)
