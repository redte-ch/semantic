from __future__ import annotations

import enum
import functools
import sys

import invoke
from invoke import Collection, Program
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout

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


class Theme(str, enum.Enum):
    WORK = "magenta"
    INFO = "cyan"
    WARN = "yellow"
    OKAY = "green"
    FAIL = "red"

    BORDER = "cyan"
    COLUMN = "magenta"
    ROW = "cyan"
    TITLE = "bold green"


class CLI(Program):

    layout = Layout()
    rows = Layout()
    grid = functools.partial(Layout, " ", ratio = 2)
    box = functools.partial(Layout, ratio = 5)
    tasks = Collection()
    console = Console()

    def __init__(self) -> None:
        self.tasks.add_task(check_deprecated)
        self.tasks.add_task(check_version)
        super().__init__(namespace = self.tasks)

    def print_help(self) -> None:
        panel = self._panel()
        content = self._content()
        self.console.print(self._layout(panel(content)))

    def task_list_opener(self, extra: str = "") -> str:
        return "Commands"

    def _layout(self, panel: Panel) -> Layout:
        self.rows.split_column(
            self.grid(),
            self.box(panel),
            self.grid(),
            )

        self.layout.split_row(
            self.grid(),
            self.box(self.rows),
            self.grid(),
            )

        return self.layout

    def _panel(self) -> Panel:
        title = self._title()
        panel = functools.partial(Panel, title = title)
        panel = functools.partial(panel, border_style = Theme.BORDER)
        panel = functools.partial(panel, padding = 1)
        return panel

    def _title(self) -> Text:
        title = (f"Usage: {self.binary} <command> [--command-opts] …\n")
        text = Text(title)
        text.stylize(Theme.TITLE)
        return text

    def _content(self) -> Table:
        table = functools.partial(Table)
        table = functools.partial(table, box = None)
        table = functools.partial(table, padding = (0,5))
        table = functools.partial(table, row_styles = [Theme.ROW])
        table = functools.partial(table, style = Theme.COLUMN)
        table = table()
        table.add_column("Command")
        table.add_column("Description")

        for command, description in self._make_pairs(self.scoped_collection):
            table.add_row(command, description)

        return table


cli = CLI()
