# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""A collection od tasks.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from invoke import Collection

from ._check_deprecated import check_deprecated
from ._check_version import check_version


class Tasks(Collection):
    """Interfaces with :mod:`.invoke` to register tasks."""

    def __init__(self) -> None:
        super().__init__()
        self.add_task(check_deprecated)
        self.add_task(check_version)
