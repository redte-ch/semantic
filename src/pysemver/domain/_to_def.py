# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

import classes


@classes.typeclass
def to_def(instance) -> str:
    """An argument's default value.

    Please note that ``None`` is always treated literally.

    Args:
        instance: Value of the return.

    Examples:
        >>> to_def("1")
        '1'

        >>> to_def(1)
        Traceback (most recent call last):
        NotImplementedError: Missing matched typeclass instance for type: int

        >>> to_def("None")
        'None'

        >>> to_def(None)
        None

    .. versionadded:: 1.0.0

    """


@to_def.instance(str)
def _from_str(instance: str) -> str:
    return instance


@to_def.instance(None)
def _from_none(instance: None) -> None:
    return instance
