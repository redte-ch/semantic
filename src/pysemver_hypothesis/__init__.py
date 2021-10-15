# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import classes
from hypothesis import strategies
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from pysemver import domain

layout_strategy = strategies.builds(
    Layout,
    strategies.text(),
    name = strategies.text(),
    size = strategies.integers(),
    minimum_size = strategies.integers(),
    ratio = strategies.integers(),
    visible = strategies.booleans(),
    )

panel_strategy = strategies.builds(
    Panel,
    strategies.text(),
    title = strategies.text(),
    subtitle = strategies.text(),
    )

table_strategy = strategies.builds(
    Table,
    strategies.text(),
    )

signature_strategy = strategies.builds(
    domain.Signature,
    name = strategies.text(),
    file = strategies.text(),
    )


@classes.typeclass
def register(instance) -> None:
    """Register an hypothesis strategy.

    Args:
        instance: The strategy to register.

    Examples:
        >>> register(Panel(str()))
        None

    .. versionadded:: 1.0.0

    """


@register.instance(Layout)
def _from_layout(instance: Layout) -> None:
    strategies.register_type_strategy(Layout, layout_strategy)


@register.instance(Panel)
def _from_panel(instance: Panel) -> None:
    strategies.register_type_strategy(Panel, panel_strategy)


@register.instance(Table)
def _from_table(instance: Table) -> None:
    strategies.register_type_strategy(Table, table_strategy)
