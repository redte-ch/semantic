from typing import Sequence

import deal
import numpy

from pysemver._types import DataclassLike

limit = 2e5
"""Just a random size/length sentinel."""


@deal.post(lambda result: result >= 0)
@deal.pre(lambda _: _.that >= 0)
@deal.pre(lambda _: _.this >= 0)
@deal.pure
def add(this: int, that: int) -> int:
    return max(that - this, 0)


@deal.pre(lambda _: limit > _.what >= 0)
@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def pre(this: int, that: int, what: int) -> numpy.ndarray:
    times: int = min(this, that)
    return numpy.repeat(what, times)


@deal.pre(lambda _: limit > _.what >= 0)
@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def rep(this: int, that: int, what: int) -> numpy.ndarray:
    times: int = max(add(this, that), add(that, this))
    return numpy.repeat(what, times)


@deal.pre(lambda _: limit > _.what >= 0)
@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def pop(this: int, that: int, what: int) -> Sequence[numpy.int_]:
    return [*pre(this, that, what), *rep(this, that, what)]


@deal.pre(lambda _: limit > _.that > 0)
@deal.pre(lambda _: limit > _.this > 0)
@deal.pure
def fill(this: int, that: int, what: DataclassLike) -> numpy.ndarray:
    max_size: int = max(this, that)
    return numpy.array([what] * max_size)
