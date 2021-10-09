from dataclasses import dataclass
from enum import Enum


class _Common(str, Enum):
    FAIL = "red"
    INFO = "cyan"
    OKAY = "green"
    TEXT = "white"
    WARN = "yellow"
    WORK = "magenta"


class _Console(str, Enum):
    BORDER = "cyan"
    HEADER = "magenta"
    ROW = "cyan"
    TITLE = "bold green"


@dataclass(frozen = True)
class Theme:
    Common = _Common
    Console = _Console
