# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import List, Tuple

import deal
import pipeop
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import _fn
from ._repo import Repo
from ._theme import Theme

_grid = _fn.partial(Layout, " ", ratio = 2)
_main = _fn.partial(Layout, ratio = 5)


@deal.pure
def _rows(panel: Panel) -> Layout:
    layout = Layout()

    layout.split_column(_grid(), _main(panel), _grid())

    return layout


@deal.pure
def _columns(panel: Layout) -> Layout:
    layout = Layout()

    layout.split_row(_grid(), _main(panel), _grid())

    return layout


class Home:
    """Home view."""

    columns = "Command", "Description"

    @deal.pure
    @pipeop.pipes
    def root(main: Panel) -> Layout:
        """Global home container."""

        return main >> _rows >> _columns

    def main(content: Table) -> Panel:
        return Panel(
            content,
            border_style = Theme.Console.BORDER,
            padding = 5,
            title = Home.usage(),
            subtitle = Repo.Version.this(),
            )

    @pipeop.pipes
    def content(tasks: List[Tuple[str, str]]) -> Table:
        """Main cli content.

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

        Home.columns << map(table.add_column) >> tuple

        tasks << _fn.dfp(table.add_row) >> tuple

        return table

    @deal.pure
    @pipeop.pipes
    def usage() -> Text:
        """A title.

        Examples:
            >>> title("name")
            <text 'Usage: name <command> [--help] …'...

        """

        text = (
            __name__
            >> str.split(".")
            >> _fn.first
            << str.format("Usage: {} [--help] <command> …")
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text


class Help:
    """Help view."""

    columns = "Flags", "Description", "Default"

    @deal.pure
    @pipeop.pipes
    def root(main: Panel) -> Layout:
        """Global help container."""

        return main >> _rows >> _columns

    @deal.pure
    @pipeop.pipes
    def main(command: str, content: Table) -> Panel:
        return Panel(
            content,
            border_style = Theme.Console.BORDER,
            padding = 5,
            title = Help.usage(command),
            subtitle = Repo.Version.this(),
            )

    @deal.pure
    @pipeop.pipes
    def content(description: str, options: [Tuple[str, ...]]) -> Table:
        """Task table.

        Examples:

        >>> content()
        "asd"

        """

        table = Table(
            box = None,
            padding = (0, 5, 1, 10),
            row_styles = [Theme.Console.ROW],
            style = Theme.Console.HEADER,
            title = description,
            )

        Help.columns << map(table.add_column) >> tuple

        options << map(table.add_row) >> tuple

        return table

    @deal.pure
    @pipeop.pipes
    def usage(command: str) -> Text:
        """A title.

        Examples:
            >>> title("name")
            <text 'Usage: name <command> [--help] …'...

        """

        text = (
            __name__
            >> str.split(".")
            >> _fn.first
            << _fn.partial(str.format("Usage: {} {} [--options] …"))
            << _fn.partial(command)
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text
