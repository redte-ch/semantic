# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Common types.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

import sys

if sys.version_info >= (3, 8):
    from typing import Literal

else:
    from typing_extensions import Literal


What = Literal["this", "that"]
