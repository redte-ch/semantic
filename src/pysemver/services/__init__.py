from hypothesis import strategies

from pysemver.domain import Signature

strategy = strategies.builds(
    Signature,
    name = strategies.just("count"),
    file = strategies.just("file.py"),
    )

strategies.register_type_strategy(Signature, strategy)
