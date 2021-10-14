# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import classes


@classes.typeclass
def default(instance) -> str:
    """An argument's default value.

    Please note that ``None`` is always treated literally.

    Args:
        instance: Value of the return.

    Examples:
        >>> default("1")
        '1'

        >>> default(1)
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: int

        >>> default("None")
        'None'

        >>> default(None)
        None

    .. versionadded:: 1.0.0

    """


@default.instance(str)
def _default_str(instance: str) -> str:
    return instance


@default.instance(None)
def _default_none(instance: None) -> None:
    return instance
