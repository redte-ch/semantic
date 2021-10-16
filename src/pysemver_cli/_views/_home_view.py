# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Home screen view.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Sequence, Tuple

import deal
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import pysemver_hypothesis as st
from pysemver import __name__, utils

from .. import __version__
from ._base import columns, rows
from ._theme import Theme

st.register(Layout, st.layouts)
st.register(Panel, st.panels)
st.register(Table, st.tables)

_headers = "Command", "Description"
#: Main command headers.

_console = Console()
#: Internal function used to render.


@deal.has("stdout")
@deal.safe
@utils.pipes
def render(tasks: Sequence[Tuple[str, str]]) -> None:
    """Render the home view.

    Args:
        tasks:
            A sequence of tuples containing the commands and their
            descriptions, default values, for each command.

    Returns:
        Nothing.

    Examples:
        >>> render([("say-hi!", "HI!!! ❤ ❤ ❤")])
        ...say-hi!...HI!!! ❤ ❤ ❤...

    .. versionadded:: 1.0.0

    """

    return (
        tasks
        >> _content
        >> _main
        >> _root
        >> _console.print
        )


@deal.pure
@utils.pipes
def _root(main: Panel) -> Layout:
    """Global home container.

    Args:
        main: Main container to wrap.

    Returns:
        Layout: To render.

    Examples:
        >>> content = _content(())
        >>> main = _main(content)
        >>> _root(main)
        Layout()

    .. versionadded:: 1.0.0

    """

    return main >> rows >> columns


@deal.pure
@utils.pipes
def _main(content: Table) -> Panel:
    """The main container, or panel.

    Args:
        content: The inner container.

    Returns:
        The outer panel.

    Examples:
        >>> content = _content(())
        >>> main = _main(content)
        >>> main.title
        ...pysemver...

    .. versionadded:: 1.0.0

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
def _content(tasks: Sequence[Tuple[str, str]]) -> Table:
    """Inner usage instructions content.

    Args:
        tasks:
            A sequence of tuples containing the commands and their
            descriptions, default values, for each command.

    Returns:
        The main content.

    Examples:
        >>> content = _content([("say-hi!", "HI!!! ❤ ❤ ❤")])
        >>> list(map(lambda option: option._cells, content.columns))
        [['say-hi!'], ['HI!!! ❤ ❤ ❤']]

    .. versionadded:: 1.0.0

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
        << utils.dmap(table.add_row)
        >> tuple
        )

    return table


@deal.pure
@utils.pipes
def _usage() -> Text:
    """Usage instructions.

    Returns:
        A formatted usage text.

    Examples:
        >>> _usage()
        <text 'Usage: pysemver [--help] <command> …' ...>

    .. versionadded:: 1.0.0

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
