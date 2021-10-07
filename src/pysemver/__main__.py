from __future__ import annotations

import sys

import pysemver as tasks

from pysemver import Bar, SupportsProgress

from ._types import HasExit


if __name__ == "__main__":
    bar: SupportsProgress = Bar()
    task: HasExit = tasks.__getattribute__(sys.argv[1])(bar)
    task()
    sys.exit(task.exit.value)
