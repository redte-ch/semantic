from __future__ import annotations

from invoke import Program
from pipeop import pipes
from rich.console import Console

from . import _ui as ui
from ._tasks import Tasks


class Main(Program):

    tasks = Tasks()
    write = Console().print

    def __init__(self) -> None:
        super().__init__(namespace = self.tasks)

    @pipes
    def print_help(self) -> None:
        (
            self.scoped_collection
            >> self._make_pairs
            >> ui.table
            >> ui.panel
            >> ui.layout
            >> self.write
            )

    def task_list_opener(self, __: str = "") -> str:
        return "Commands"


main = Main()
