# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

"""Views, or interface, of pysemver.

Loosely based on the MVC thing, the idea is to have a clear separation of
concerns between the presentation layer and the rest of the package. Views
are mostly repetitive, but it is yet too soon to refactor them.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import List, Tuple

import deal
import pipeop
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import utils
from ._repo import Repo
from ._theme import Theme

_grid = utils.partial(Layout, " ", ratio = 2)
"""To fill around the terminal."""

_main = utils.partial(Layout, ratio = 5)
"""To render the main cli view."""


@pipeop.pipes
def _rows(panel: Panel) -> Layout:
    """Splits the terminal horizontally."""

    return (
        Layout()
        << utils.partial(Layout.split_column)
        >> utils.partial(_grid())
        >> utils.partial(_main(panel))
        >> utils.partial(_grid())
        >> utils.do
        )


@pipeop.pipes
def _columns(panel: Layout) -> Layout:
    """Splits the terminal vertically."""

    return (
        Layout()
        << utils.partial(Layout.split_row)
        >> utils.partial(_grid())
        >> utils.partial(_main(panel))
        >> utils.partial(_grid())
        >> utils.do
        )


class Home:
    """Home screen view."""

    columns = "Command", "Description"
    """Main command columns."""

    @pipeop.pipes
    def root(main: Panel) -> Layout:
        """Global home container.

        Args:
            main: Main container to wrap.

        Returns:
            Layout: To render.

        Examples:
            >>> Home.root(Panel("Hey!"))
            Layout()

        """

        return main >> _rows >> _columns

    def main(content: Table) -> Panel:
        """The main container, or panel.

        Args:
            content: The inner container.

        Returns:
            The outer panel.

        Examples:
            >>> main()

        """

        return Panel(
            content,
            border_style = Theme.Console.BORDER,
            padding = 5,
            title = Home.usage(),
            subtitle = Repo.Version.this(),
            )

    @deal.pure
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

        (
            Home.columns
            << map(table.add_column)
            << tuple
            )

        tasks << utils.dfp(table.add_row) >> tuple

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
            >> utils.first
            << str.format("Usage: {} [--help] <command> …")
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text


class Help:
    """Help view."""

    columns = "Flags", "Description", "Default values"

    @pipeop.pipes
    def root(main: Panel) -> Layout:
        """Global help container."""

        return main >> _rows >> _columns

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
            )

        (
            Help.columns
            << map(table.add_column)
            << tuple
            )

        (
            options
            >> utils.dfc()
            << utils.dfp(table.add_row)
            << tuple
            )

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
            >> utils.first
            << str.format("Usage: {1} {0} [--options] …", command)
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text
