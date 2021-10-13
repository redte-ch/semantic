import deal
import numpy
from hypothesis import strategies

from pysemver.domain import Signature

limit = 2e5
"""Just a random size/length sentinel."""


strategy = strategies.builds(
    Signature,
    name = strategies.just("count"),
    file = strategies.just("file.py"),
    )

strategies.register_type_strategy(Signature, strategy)


@deal.pure
def add(this: int, that: int) -> int:
    return max(that - this, 0)


@deal.pre(lambda _: limit > _.what >= 0)
@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def repeat(this: int, that: int, what: int) -> numpy.ndarray:
    times: int = max(add(this, that), add(that, this))
    return numpy.repeat(what, times)


@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def fill(this: int, that: int, what: Signature) -> numpy.ndarray:
    max_size: int = max(this, that)
    return numpy.array([what] * max_size)
