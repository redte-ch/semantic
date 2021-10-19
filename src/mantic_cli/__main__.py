# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Main cli initialiser.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import cast, Tuple

import inspect

import typic
from invoke import Program

import mantic_cli

from .tasks import Tasks
from .views import help_view, home_view, to_options

_tasks: Tasks = Tasks()
#: The list of tasks.

_header: str = "Commands"
#: The home screen header opener.


@typic.klass(always = True, strict = True)
class Main(Program):
    """Interfaces with :mod:`.invoke`."""

    def __init__(self) -> None:
        super().__init__(
            namespace = _tasks,
            version = mantic_cli.__version__,
            )

    def print_help(self) -> None:
        """Intercepts :mod:`.invoke` to print the home screen."""

        return home_view.render(self._make_pairs(_tasks))

    def print_task_help(self, command: str) -> None:
        """Intercepts :mod:`.invoke` to print the help screen."""

        doc: str
        options: Tuple[Tuple[str, ...], ...]

        doc = cast(str, inspect.getdoc(_tasks[command]))
        context = self.parser.contexts[command]
        options = to_options(context.help_tuples())

        return help_view.render(command, doc, options)

    def task_list_opener(self, _command: str = "") -> str:
        """Intercepts :mod:`.invoke` to set the main header name."""

        return _header


main = Main()
