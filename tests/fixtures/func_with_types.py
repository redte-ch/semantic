# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from typing import Any, List, Tuple, Union


def function(
        a: int,
        *,
        b: int,
        c,
        d,
        ) -> Union[List[int], Tuple[Any, ...]]:
    ...
