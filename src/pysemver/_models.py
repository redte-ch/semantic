from __future__ import annotations

from typing import Optional, Sequence, Tuple

from typic import klass


@klass(frozen = True, slots = True, strict = True)
class ArgType:
    """An argument type."""

    name: str


@klass(frozen = True, slots = True, strict = True)
class RetType:
    """A return type."""

    name: str


@klass(frozen = True, slots = True, strict = True)
class Argument:
    """An argument."""

    name: str
    types: Optional[Tuple[ArgType, ...]] = None
    default: Optional[str] = None


@klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature, that is arguments and returns."""

    name: str
    file: str
    arguments: Sequence[Argument] = ()
    returns: Optional[Sequence[RetType]] = None
