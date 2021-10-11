# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

import functools
from typing import List, Tuple

import cytoolz
import deal
import pipeop
import typic
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ._repo import Repo
from ._theme import Theme

_grid = functools.partial(Layout, " ", ratio = 2)

_main = functools.partial(Layout, ratio = 5)


@deal.pure
def _rows(panel: Panel) -> Layout:
    layout = Layout()

    layout.split_column(_grid(), _main(panel), _grid())

    return layout


@deal.pure
@typic.al(strict = True)
def _columns(panel: Layout) -> Layout:
    layout = Layout()

    layout.split_row(_grid(), _main(panel), _grid())

    return layout


@typic.klass(frozen = True, slots = True, strict = True)
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

        tasks << map(lambda task: table.add_row(*task)) >> tuple

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
            >> cytoolz.first
            << str.format("Usage: {} [--help] <command> …")
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text


@typic.klass(frozen = True, slots = True, strict = True)
class Help:
    """Help view."""

    columns = "Flags", "Description", "Default"

    @deal.pure
    @pipeop.pipes
    #  @typic.al(strict = True)
    #  https://github.com/seandstewart/typical/issues/183
    def root(main: Panel) -> Layout:
        """Global help container."""

        return main >> _rows >> _columns

    #  @typic.al(strict = True)
    #  https://github.com/seandstewart/typical/issues/183
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
            >> cytoolz.first
            << functools.partial(str.format("Usage: {} {} [--options] …"))
            << functools.partial(command)
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text
