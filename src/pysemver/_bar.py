# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

import sys
from typing import Sequence

import deal
import termcolor

WORK_ICON: str = termcolor.colored("[/]", "cyan")
INFO_ICON: str = termcolor.colored("[i]", "cyan")
WARN_ICON: str = termcolor.colored("[!]", "yellow")
OKAY_ICON: str = termcolor.colored("[✓]", "green")
FAIL_ICON: str = termcolor.colored("[x]", "red")

BAR_ICON: str = termcolor.colored("|", "green")
ACC_ICON: str = termcolor.colored("✓", "green")
ETA_ICON: str = termcolor.colored("·", "green")

BAR_SIZE: int = 50


class Bar:
    """Provides a progress bar for tasks.

    .. versionadded:: 1.0.0

    """

    @deal.safe
    @deal.has("stdout")
    def init(self) -> None:
        """Initialises the progress bar."""

        sys.stdout.write(self._init_message())

    @deal.safe
    @deal.has("stdout")
    def push(self, count: int, total: int) -> None:
        """Pushes progress to the ``stdout``."""

        done: int = (count + 1) * 100 // total
        sys.stdout.write(self._push_message(done))

    @deal.safe
    @deal.has("stdout")
    def okay(self, message: str) -> None:
        """Prints an okay ``message``."""

        sys.stdout.write(f"{OKAY_ICON} {message}")

    @deal.safe
    @deal.has("stdout")
    def info(self, message: str) -> None:
        """Prints an info ``message``."""

        sys.stdout.write(f"{INFO_ICON} {message}")

    @deal.safe
    @deal.has("stdout")
    def warn(self, message: str) -> None:
        """Prints a warn ``message``."""

        sys.stdout.write(f"{WARN_ICON} {message}")

    @deal.safe
    @deal.has("stdout")
    def fail(self) -> None:
        """Marks last printed message as failing."""

        sys.stdout.write(f"\r{FAIL_ICON}")

    @deal.safe
    @deal.has("stdout")
    def then(self) -> None:
        """Prints a new line and resets the cursor position."""

        sys.stdout.write("\n\r")

    @deal.safe
    @deal.has("stdout")
    def wipe(self) -> None:
        """Cleans last printed message."""

        sys.stdout.write(self._wipe_message())

    @deal.pure
    def _init_message(self) -> str:
        message: Sequence[str]
        message = [
            f"{WORK_ICON} 0%   {BAR_ICON}",
            f"{ETA_ICON * BAR_SIZE}{BAR_ICON}\r",
            ]

        return "".join(message)

    @deal.pure
    def _push_message(self, done: int) -> str:
        message: Sequence[str]
        spaces: str

        spaces = ""
        spaces += [" ", ""][done >= BAR_SIZE * 2]
        spaces += [" ", ""][done >= BAR_SIZE // 5]

        message = [
            f"{WORK_ICON} {done}% {spaces}{BAR_ICON}"
            f"{ACC_ICON * (done // 2)}"
            f"{ETA_ICON * (BAR_SIZE - done // 2)}"
            f"{BAR_ICON}\r"
            ]

        return "".join(message)

    @deal.pure
    def _wipe_message(self) -> str:
        return f"{' ' * BAR_SIZE * 3}\r"
