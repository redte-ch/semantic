# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Shared hypothesis strategies.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import Any, Callable, Type

from hypothesis import strategies as st

F = Callable[..., Any]


def layouts(layout: Type[object]) -> st.SearchStrategy[object]:
    """A strategy for layouts."""

    return st.builds(
        layout,
        st.text(),
        name = st.text(),
        size = st.integers(),
        minimum_size = st.integers(),
        ratio = st.integers(),
        visible = st.booleans(),
        )


def panels(panel: Type[object]) -> st.SearchStrategy[object]:
    """A strategy for panels."""

    return st.builds(
        panel,
        st.text(),
        title = st.text(),
        subtitle = st.text(),
        )


def tables(table: Type[object]) -> st.SearchStrategy[object]:
    """A strategy for tables."""

    return st.builds(
        table,
        st.text(),
        )


def signatures(signature: Type[object]) -> st.SearchStrategy[object]:
    """A strategy for signatures."""

    return st.builds(
        signature,
        name = st.text(min_size = 1),
        file = st.text(min_size = 1),
        )


def register(what: Type[object], strategy: F) -> None:
    """Register an hypothesis strategy.

    Args:
        what: What to register a strategy for.
        strategy: The strategy to register.

    Examples:
        >>> from rich.panel import Panel

        >>> register(Panel, panels)
        None

    .. versionadded:: 1.0.0

    """

    st.register_type_strategy(what, strategy)
