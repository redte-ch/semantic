# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import List, Tuple

import funcy
import typic
from pipeop import pipes
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ._repo import Repo
from ._theme import Theme

grid = funcy.partial(Layout, " ", ratio = 2)
main = funcy.partial(Layout, ratio = 5)


@typic.al(strict = True)
def table(tasks: List[Tuple[str, str]]) -> Table:
    """
    Examples:

    >>> content()
    "asd"

    """

    table = Table(
        box = None,
        padding = (0, 5, 1, 10),
        row_styles = [Theme.Console.ROW],
        style = Theme.Console.HEADER,
        )

    table.add_column("Command")
    table.add_column("Description")

    for key, value in tasks:
        table.add_row(key, value)

    return table


#  @typic.al(strict = True)
#  https://github.com/seandstewart/typical/issues/183
def panel(table: Table) -> Panel:
    return Panel(
        table,
        border_style = Theme.Console.BORDER,
        padding = 5,
        title = _title(),
        subtitle = Repo.Version.this(),
        )


@pipes
#  @typic.al(strict = True)
#  https://github.com/seandstewart/typical/issues/183
def layout(panel: Panel) -> Layout:
    return panel >> _rows >> _columns


@pipes
def _title() -> Text:
    """A title.

    Examples:
        >>> title("name")
        <text 'Usage: name <command> [--help] …'...

    """

    text = (
        __name__
        >> str.split(".")
        >> funcy.first
        << str.format("Usage: {} <command> [--help] …")
        >> Text
        )

    text.stylize(Theme.Console.TITLE)

    return text


def _rows(panel: Panel) -> Layout:
    layout = Layout()

    layout.split_column(grid(), main(panel), grid())

    return layout


def _columns(panel: Layout) -> Layout:
    layout = Layout()

    layout.split_row(grid(), main(panel), grid())

    return layout
