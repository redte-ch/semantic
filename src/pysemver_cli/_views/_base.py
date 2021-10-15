# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Views, or interface, of pysemver.

Loosely based on the MVC thing, the idea is to have a clear separation of
concerns between the presentation layer and the rest of the package. Views
are mostly repetitive, but it is yet too soon to refactor them.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import aenum
from aenum import Enum
from rich.layout import Layout
from rich.panel import Panel

from pysemver import utils

_grid = utils.partial(Layout, " ", ratio = 2)
"""To fill around the terminal."""

_main = utils.partial(Layout, ratio = 5)
"""To render the main cli view."""


@utils.pipes
def rows(panel: Panel) -> Layout:
    """Splits the terminal horizontally."""

    return (
        Layout()
        << utils.partial(Layout.split_column)
        >> utils.partial(_grid())
        >> utils.partial(_main(panel))
        >> utils.partial(_grid())
        >> utils.do
        )


@utils.pipes
def columns(panel: Layout) -> Layout:
    """Splits the terminal vertically."""

    return (
        Layout()
        << utils.partial(Layout.split_row)
        >> utils.partial(_grid())
        >> utils.partial(_main(panel))
        >> utils.partial(_grid())
        >> utils.do
        )


class Theme(Enum):

    @aenum.skip
    class Common(str, Enum):
        FAIL = "red"
        INFO = "cyan"
        OKAY = "green"
        TEXT = "white"
        WARN = "yellow"
        WORK = "magenta"

    @aenum.skip
    class Console(str, Enum):
        BORDER = "cyan"
        HEADER = "magenta"
        ROW = "cyan"
        TITLE = "bold green"
