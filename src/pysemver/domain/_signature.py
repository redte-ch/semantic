# @typic.klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature, that is arguments and returns."""

    name: str
    file: str
    # arguments: Sequence[Argument] = ()
    # returns: Optional[Sequence[RetType]] = None
