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

from . import _fn
from ._repo import Repo
from ._theme import Theme

_grid = _fn.partial(Layout, " ", ratio = 2)
"""To fill around the terminal."""

_main = _fn.partial(Layout, ratio = 5)
"""To render the main cli view."""


@deal.pure
@pipeop.pipes
def _rows(panel: Panel) -> Layout:
    """Splits the terminal horizontally."""

    return (
        Layout()
        << _fn.partial(Layout.split_column)
        >> _fn.partial(_grid())
        >> _fn.partial(_main(panel))
        >> _fn.partial(_grid())
        >> _fn.do
        )


@deal.pure
@pipeop.pipes
def _columns(panel: Layout) -> Layout:
    """Splits the terminal vertically."""

    return (
        Layout()
        << _fn.partial(Layout.split_row)
        >> _fn.partial(_grid())
        >> _fn.partial(_main(panel))
        >> _fn.partial(_grid())
        >> _fn.do
        )


class Home:
    """Home screen view."""

    columns = "Command", "Description"
    """Main command columns."""

    @deal.pure
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

    columns = "Flags", "Description", "Default values"

    @deal.pure
    @pipeop.pipes
    def root(main: Panel) -> Layout:
        """Global help container."""

        return main >> _rows >> _columns

    # @deal.pure
    @pipeop.pipes
    def main(command: str, content: Table) -> Panel:
        return Panel(
            content,
            border_style = Theme.Console.BORDER,
            padding = 5,
            title = Help.usage(command),
            subtitle = Repo.Version.this(),
            )

    # @deal.pure
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
            >> _fn.dfc()
            << _fn.dfp(table.add_row)
            << tuple
            )

        return table

    # @deal.pre(lambda command: isinstance(command, str))
    @pipeop.pipes
    def usage(command: str) -> Text:
        """A title.

        Examples:
            >>> title("name")
            <text 'Usage: name <command> [--help] …'...

        """

        # breakpoint()

        text = (
            __name__
            >> str.split(".")
            >> _fn.first
            << str.format("Usage: {1} {0} [--options] …", command)
            >> Text
            )

        text.stylize(Theme.Console.TITLE)

        return text
