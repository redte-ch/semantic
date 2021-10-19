# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Help view.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Tuple

import deal
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import mantic_hypothesis as st
from mantic import __name__, utils

from .. import __version__
from ._base import columns, rows
from ._theme import ThemeConsole

st.register(Layout, st.layouts)
st.register(Panel, st.panels)
st.register(Table, st.tables)

_headers = "Flags", "Description", "Default values"
#: Help command headers.

_console = Console()
#: Internal function used to render.


@deal.has("stdout")
@deal.safe
def render(
        command: str,
        doc: str,
        options: Tuple[Tuple[str, ...], ...],
        ) -> None:
    """Render the home view.

    Args:
        command:
            The name of the task.
        doc:
            The documentation of the task.
        options:
            A sequence of tuples containing the commands and their
            descriptions, default values, for each command.

    Examples:
        >>> command = "say-hi!"
        >>> doc = "How to say hi."
        >>> options = [("-f --flag", "How?", "Like that!")]
        >>> render(command, doc, options)
        ...say-hi!...How to say hi...-f --flag...How?...Like that!...

    .. versionadded:: 1.0.0

    """

    content = _content(doc, options)
    main = _main(command, content)
    root = _root(main)

    _console.print(root)


@deal.pure
def _root(main: Panel) -> Layout:
    """Global help container.

    Args:
        main: Main container to wrap.

    Returns:
        Layout: To render.

    Examples:
        >>> content = _content("", ())
        >>> main = _main("command", content)
        >>> _root(main)
        Layout()

    .. versionadded:: 1.0.0

    """

    return columns(rows(main))


@deal.pure
def _main(command: str, content: Table) -> Panel:
    """Main help container.

    Args:
        command: The name of the task.
        content: The inner container.

    Returns:
        The outer panel.

    Examples:
        >>> content = _content("", ())
        >>> main = _main("command", content)
        >>> main.title
        ...command...

    .. versionadded:: 1.0.0

    """

    return Panel(
        content,
        border_style = ThemeConsole.BORDER,
        padding = 5,
        title = _usage(command),
        subtitle = __version__,
        )


@deal.pure
def _content(doc: str, options: Tuple[Tuple[str, ...], ...]) -> Table:
    """Inner usage instructions content.

    Args:
        doc:
            The documentation of the task.
        options:
            A sequence of triples containing the flags, descriptions, and
            default values, for each option.

    Returns:
        The main content.

    Examples:
        >>> doc = "How to say hi."
        >>> options = [("-f --flag", "How?", "Like that!")]
        >>> content = _content(doc, options)
        >>> list(map(lambda option: option._cells, content.columns))
        [['-f --flag'], ['How?'], ['Like that!']]

        >>> content = _content("", [("", "", "")])
        >>> list(map(lambda option: option._cells, content.columns))
        [[''], [''], ['']]

    .. versionadded:: 1.0.0

    """

    table = Table(
        box = None,
        padding = (0, 5, 1, 10),
        row_styles = [ThemeConsole.ROW],
        style = ThemeConsole.HEADER,
        title = f"{doc}\n\n\n",
        )

    list(map(table.add_column, _headers))

    list(utils.dmap(table.add_row, options))

    return table


@deal.pure
def _usage(command: str) -> Text:
    """Usage instructions.

    Args:
        command: The name of the task.

    Returns:
        A formatted usage text.

    Examples:
        >>> _usage("command")
        <text 'Usage: mantic command [--options] …' ...>

    .. versionadded:: 1.0.0

    """

    text = Text(f"Usage: {__name__} {command} [--options] …")

    text.stylize(ThemeConsole.TITLE)

    return text
