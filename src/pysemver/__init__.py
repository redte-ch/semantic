# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from hypothesis import strategies

from . import _infra as infra  # noqa: F401
from . import _utils as utils
from ._types import DataclassLike

strategies.register_type_strategy(DataclassLike, utils.dataclass_strategy)
