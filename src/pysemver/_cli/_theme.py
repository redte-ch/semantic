# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from aenum import Enum, skip


class Theme(Enum):

    @skip
    class Common(str, Enum):
        FAIL = "red"
        INFO = "cyan"
        OKAY = "green"
        TEXT = "white"
        WARN = "yellow"
        WORK = "magenta"

    @skip
    class Console(str, Enum):
        BORDER = "cyan"
        HEADER = "magenta"
        ROW = "cyan"
        TITLE = "bold green"
