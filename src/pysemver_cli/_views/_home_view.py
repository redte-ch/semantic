# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Home screen view.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import List, Tuple

import deal
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import pysemver
from pysemver import utils

from .. import __version__
from ._base import columns, rows, Theme

_headers = "Command", "Description"
"""Main command headers."""


@utils.pipes
def _root(main: Panel) -> Layout:
    """Global home container.

    Args:
        main: Main container to wrap.

    Returns:
        Layout: To render.

    Examples:
        >>> Home.root(Panel("Hey!"))
        Layout()

    """

    return main >> rows >> columns


def _main(content: Table) -> Panel:
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
        title = _usage(),
        subtitle = __version__,
        )


@deal.pure
@utils.pipes
def _content(tasks: List[Tuple[str, str]]) -> Table:
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
        _headers
        << map(table.add_column)
        << tuple
        )

    (
        tasks
        << utils.dfp(table.add_row)
        >> tuple
        )

    return table


@deal.pure
@utils.pipes
def _usage() -> Text:
    """Usage instructions.

    Examples:
        >>> _usage()
        <text 'Usage: pysemver [--help] <command> …' ...>

    """

    text = (
        pysemver.__name__
        >> str.split(".")
        >> utils.first
        << str.format("Usage: {} [--help] <command> …")
        >> Text
        )

    text.stylize(Theme.Console.TITLE)

    return text
