# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

# @typic.klass(frozen = True, slots = True, strict = True)
class Signature:
    """A signature, that is arguments and returns."""

    name: str
    file: str
    # arguments: Sequence[Argument] = ()
    # returns: Optional[Sequence[RetType]] = None
