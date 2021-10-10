# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

import sys

import invoke
from invoke import Collection

from ._check_deprecated import CheckDeprecated
from ._check_version import CheckVersion
from ._types import HasExit
from ._bar import Bar


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

    @invoke.task
    def check_version(_context):
        """Check if the actual version is valid."""

        task: HasExit
        task = CheckVersion(Tasks.bar)
        task()
        sys.exit(task.exit.value)
