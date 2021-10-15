# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import inspect

from invoke import Program

import pysemver_cli
from pysemver import utils

from ._tasks import Tasks
from ._views import help_view, home_view, to_options


class Main(Program):

    tasks = Tasks()

    def __init__(self) -> None:
        super().__init__(
            namespace = self.tasks,
            version = pysemver_cli.__version__,
            )

    @utils.pipes
    def print_help(self) -> None:
        self.scoped_collection >> self._make_pairs >> home_view.render

    @utils.pipes
    def print_task_help(self, command: str) -> None:
        context = self.parser.contexts >> dict.get(command)
        task = self.collection >> Tasks.__getitem__(command)
        doc = inspect.getdoc(task)
        context.help_tuples() >> to_options << help_view.render(command, doc)

    def task_list_opener(_self, _name: str = "") -> str:
        return "Commands"


main = Main()
