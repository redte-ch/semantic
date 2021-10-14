# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from hypothesis import strategies

from .__main__ import main  # noqa: F401
from ._types import DataclassLike
from .utils import dataclass_strategy

strategies.register_type_strategy(DataclassLike, dataclass_strategy)
