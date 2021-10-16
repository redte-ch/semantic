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

import pysemver_hypothesis
from pysemver import utils

pysemver_hypothesis.register(Layout(""))
pysemver_hypothesis.register(Panel(""))

_grid = utils.partial(Layout, " ", ratio = 2)
#: To fill around the terminal.

_main = utils.partial(Layout, ratio = 5)
#: To render the main cli view.


@deal.pure
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


@deal.pure
@utils.pipes
def columns(layout: Layout) -> Layout:
    """Splits the terminal vertically."""

    return (
        Layout()
        << utils.partial(Layout.split_row)
        >> utils.partial(_grid())
        >> utils.partial(_main(layout))
        >> utils.partial(_grid())
        >> utils.do
        )
