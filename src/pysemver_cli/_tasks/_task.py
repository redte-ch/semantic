# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import MutableMapping, Tuple

import typic


@typic.klass(frozen = True, slots = True, strict = True)
class Task:
    """Represents a task."""

    optional: Tuple[str]
    help: MutableMapping[str, Tuple[str, ...]]
