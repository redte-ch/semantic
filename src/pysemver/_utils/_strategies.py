# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from hypothesis import strategies

from .._types import DataclassLike

dataclass_strategy = strategies.builds(
    DataclassLike,
    some = strategies.just("some"),
    thing = strategies.just("thing"),
    )
