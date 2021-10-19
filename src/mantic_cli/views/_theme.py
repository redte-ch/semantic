# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""CLI theme.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from enum import Enum


class ThemeCommon(str, Enum):
    """Common theme for the whole cli."""

    FAIL = "red"
    INFO = "cyan"
    OKAY = "green"
    TEXT = "white"
    WARN = "yellow"
    WORK = "magenta"


class ThemeConsole(str, Enum):
    """Specific rendering theme for instruction screens."""

    BORDER = "cyan"
    HEADER = "magenta"
    ROW = "cyan"
    TITLE = "bold green"
