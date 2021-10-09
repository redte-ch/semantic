from __future__ import annotations

import sys

import invoke
from invoke import Collection, Program

from pysemver import Bar, SupportsProgress
from pysemver import CheckDeprecated, CheckVersion

from ._types import HasExit

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


class Console(Program):

    tasks = Collection()

    def __init__(self) -> None:
        self.tasks.add_task(check_deprecated)
        self.tasks.add_task(check_version)
        super().__init__(namespace = self.tasks)

    def print_help(self) -> None:
        usage = "<command> [--command-opts] ..."
        sys.stdout.write(f"Usage: {self.binary} {usage}\n")
        sys.stdout.write("\n")
        self.list_tasks()

    def task_list_opener(self, extra: str = "") -> str:
        return "Commands"


console = Console()
