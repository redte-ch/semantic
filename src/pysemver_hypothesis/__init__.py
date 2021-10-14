# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from hypothesis import strategies

from pysemver.domain import Signature

signature_strategy = strategies.builds(
    Signature,
    name = strategies.text(),
    file = strategies.text(),
    )


strategies.register_type_strategy(Signature, signature_strategy)
