# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""A generic service to run terminal commands.

.. versionadded:: 1.0.0

"""


from __future__ import annotations

from typing import Sequence

import subprocess

import deal


@deal.pure
def run(cmd: Sequence[str]) -> str:
    """Runs a command an decodes the result.

    Args:
        cmd: The command to run, as a list.

    Returns:
        The decoded ``stdout``.

    Examples:
        >>> Repo.run(["echo", "1"])
        '1\\n'

    .. versionadded:: 36.1.0

    """

    return \
        subprocess \
        .run(cmd, check = True, stdout = subprocess.PIPE) \
        .stdout \
        .decode("utf-8")
