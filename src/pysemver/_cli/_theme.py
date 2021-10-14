# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import aenum
from aenum import Enum


class Theme(Enum):

    @aenum.skip
    class Common(str, Enum):
        FAIL = "red"
        INFO = "cyan"
        OKAY = "green"
        TEXT = "white"
        WARN = "yellow"
        WORK = "magenta"

    @aenum.skip
    class Console(str, Enum):
        BORDER = "cyan"
        HEADER = "magenta"
        ROW = "cyan"
        TITLE = "bold green"
