# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Provides a logger for tasks, with a progress bar!.

.. versionadded:: 1.0.0

"""


from __future__ import annotations

from typing import Sequence

import sys

import deal
import termcolor

limit = 2e5
"""Just a random size/length sentinel."""

_work_icon: str = termcolor.colored("[/]", "cyan")
_info_icon: str = termcolor.colored("[i]", "cyan")
_warn_icon: str = termcolor.colored("[!]", "yellow")
_okay_icon: str = termcolor.colored("[✓]", "green")
_fail_icon: str = termcolor.colored("[x]", "red")

_bar_icon: str = termcolor.colored("|", "green")
_acc_icon: str = termcolor.colored("✓", "green")
_eta_icon: str = termcolor.colored("·", "green")

_bar_size: int = 50


@deal.safe
@deal.has("stdout")
def init() -> None:
    """Initialises the progress bar."""

    sys.stdout.write(_init_message())


@deal.pre(lambda count, total: limit > count >= 0 and limit > total >= 0)
@deal.has("stdout")
def push(count: int, total: int) -> None:
    """Pushes progress to the ``stdout``."""

    done: int = (count + 1) * 100 // total
    sys.stdout.write(_push_message(done))


@deal.safe
@deal.has("stdout")
def okay(message: str) -> None:
    """Prints an okay ``message``."""

    sys.stdout.write(f"{_okay_icon} {message}")


@deal.safe
@deal.has("stdout")
def info(message: str) -> None:
    """Prints an info ``message``."""

    sys.stdout.write(f"{_info_icon} {message}")


@deal.safe
@deal.has("stdout")
def warn(message: str) -> None:
    """Prints a warn ``message``."""

    sys.stdout.write(f"{_warn_icon} {message}")


@deal.safe
@deal.has("stdout")
def fail() -> None:
    """Marks last printed message as failing."""

    sys.stdout.write(f"\r{_fail_icon}")


@deal.safe
@deal.has("stdout")
def then() -> None:
    """Prints a new line and resets the cursor position."""

    sys.stdout.write("\n\r")


@deal.safe
@deal.has("stdout")
def wipe() -> None:
    """Cleans last printed message."""

    sys.stdout.write(_wipe_message())


@deal.pure
def _init_message() -> str:
    message: Sequence[str]
    message = [
        f"{_work_icon} 0%   {_bar_icon}",
        f"{_eta_icon * _bar_size}{_bar_icon}\r",
        ]

    return "".join(message)


@deal.pre(lambda done: limit > done >= 0)
@deal.has()
def _push_message(done: int) -> str:
    message: Sequence[str]
    spaces: str

    spaces = ""
    spaces += [" ", ""][done >= _bar_size * 2]
    spaces += [" ", ""][done >= _bar_size // 5]

    message = [
        f"{_work_icon} {done}% {spaces}{_bar_icon}"
        f"{_acc_icon * (done // 2)}"
        f"{_eta_icon * (_bar_size - done // 2)}"
        f"{_bar_icon}\r"
        ]

    return "".join(message)


@deal.pure
def _wipe_message() -> str:
    return f"{' ' * _bar_size * 3}\r"
