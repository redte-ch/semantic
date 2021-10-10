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
