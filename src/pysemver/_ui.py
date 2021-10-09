import funcy
from pipeop import pipes
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ._theme import Theme

grid = funcy.partial(Layout, " ", ratio = 2)
main = funcy.partial(Layout, ratio = 5)


def table(tasks: tuple) -> Table:
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


def panel(table: Table) -> Panel:
    return Panel(
        table,
        border_style = Theme.Console.BORDER,
        padding = 5,
        title = _title(),
        )


@pipes
def layout(panel: Panel) -> Layout:
    return (
        panel
        >> _rows(grid, main)
        >> _columns(grid, main)
        )


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


def _rows(panel: Panel, grid: Layout, main: Layout) -> Layout:
    layout = Layout()

    layout.split_column(grid(), main(panel), grid())

    return layout


def _columns(panel: Layout, grid: Layout, main: Layout) -> Layout:
    layout = Layout()

    layout.split_row(grid(), main(panel), grid())

    return layout
