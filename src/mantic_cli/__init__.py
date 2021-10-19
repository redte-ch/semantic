# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Mantic CLI.

This sub-package contains the command-line interface of :mod:`.mantic`.

Example usage::

    mantic
    mantic check-deprecated
    mantic --help check-version

.. versionadded:: 1.0.0

"""

from mantic import __version__  # noqa: F401

from .__main__ import main  # noqa: F401
