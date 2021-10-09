from __future__ import annotations

import sys

import invoke
from invoke import Collection, Program

from pysemver import Bar, SupportsProgress
from pysemver import CheckDeprecated, CheckVersion

from ._types import HasExit

bar: SupportsProgress = Bar()
tasks = Collection()


@invoke.task
def check_deprecated(context):
    """Check if there are features to deprecate."""

    context.task: HasExit
    context.task = CheckDeprecated(bar)
    context.task()
    sys.exit(context.task.exit.value)


@invoke.task
def check_version(context):
    """Check if the actual version is valid."""

    context.task: HasExit
    context.task = CheckVersion(bar)
    context.task()
    sys.exit(context.task.exit.value)


tasks.add_task(check_deprecated)
tasks.add_task(check_version)
console = Program(namespace = tasks)
