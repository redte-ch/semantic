from __future__ import annotations

import sys

import invoke

from ._check_deprecated import CheckDeprecated
from ._check_version import CheckVersion
from ._types import HasExit
from ._bar import Bar, SupportsProgress

bar: SupportsProgress = Bar()


@invoke.task
def check_deprecated(_context):
    """Check if there are features to deprecate."""

    task: HasExit
    task = CheckDeprecated(bar)
    task()
    sys.exit(task.exit.value)


@invoke.task
def check_version(_context):
    """Check if the actual version is valid."""

    task: HasExit
    task = CheckVersion(bar)
    task()
    sys.exit(task.exit.value)
