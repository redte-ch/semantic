# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Command-line tools to facilitate semantic versioning.

.. versionadded:: 1.0.0

"""

from . import actions  # noqa: F401
from . import domain  # noqa: F401
from . import infra  # noqa: F401
from . import utils  # noqa: F401

__version__ = infra.repo.versions.this()
