# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Base elements of views.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import deal
from rich.layout import Layout
from rich.panel import Panel

import mantic_hypothesis as st
from mantic import utils

st.register(Layout, st.layouts)
st.register(Panel, st.panels)

_grid = utils.partial(Layout, " ", ratio = 2)
#: To fill around the terminal.

_main = utils.partial(Layout, ratio = 5)
#: To render the main cli view.


@deal.pure
def rows(panel: Panel) -> Layout:
    """Splits the terminal horizontally."""

    layout = Layout()

    layout.split_column(_grid(), _main(panel), _grid())

    return layout


@deal.pure
def columns(panel: Layout) -> Layout:
    """Splits the terminal vertically."""

    layout = Layout()

    layout.split_row(_grid(), _main(panel), _grid())

    return layout
