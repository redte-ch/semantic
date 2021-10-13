[![Test](https://github.com/maukoquiroga/pysemver/workflows/test/badge.svg)](https://github.com/maukoquiroga/pysemver/actions?workflow=test)
[![Type](https://github.com/maukoquiroga/pysemver/workflows/type/badge.svg)](https://github.com/maukoquiroga/pysemver/actions?workflow=type)
[![Lint](https://github.com/maukoquiroga/pysemver/workflows/lint/badge.svg)](https://github.com/maukoquiroga/pysemver/actions?workflow=lint)
[![Docs](https://github.com/maukoquiroga/pysemver/workflows/docs/badge.svg)](https://github.com/maukoquiroga/pysemver/actions?workflow=docs)
[![Docs](https://readthedocs.org/projects/pysemver/badge/)](https://pysemver.readthedocs.io/)
[![PyPI](https://img.shields.io/pypi/v/pysemver.svg)](https://pypi.org/project/pysemver/)
[![Coverage](https://codecov.io/gh/maukoquiroga/pysemver/branch/master/graph/badge.svg)](https://codecov.io/gh/maukoquiroga/pysemver)

Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>

Licensed under the EUPL-1.2-or-later
For details: [https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)

### TODO

- [ ] Structure package
  - [ ] Domain
    - [ ] Entities (contracts, has an ID)
    - [ ] Value objects (return types, arguments, ... , don't have meaning, or ID)
    - [ ] Aggregates / aggregate root (where the invariants go ...)
      - [ ] An aggregate is a collection on entity and value objects that are ONLY accessed through an aggregate root.
      - [ ] An aggregate root (AR) is an entity through which the outside world interacts with an aggregate.
      - [ ] An aggregate is a consistency boundary. All of the aggregate is loaded and stored together.
    - [ ] Domain rules
      - [ ] Contracts, en gros
      - [ ] internes
      - [ ] externes ?
  - [ ] App / application / services
    - [ ] Commands
    - [ ] Queries
    - [ ] Views ?
    - [ ] (app/domain) Services ?
  - [ ] Intra / infrastructure
    - [ ] Bar / logging
    - [ ] git/repo
    - [ ] cache
    - [ ] adapters ... 
  - [ ] Interface (cli)
    - [ ] Controllers ?
    - [ ] CLI ?
    - [ ] Main ... 
    - [ ] Views ?
  - [ ] utils
    - [ ] fn.py ...

- src
  - pysemver
    - __init__.py
    - __main__.py (entrypoint)
    - config.py
    - infra
      - repo.py
    - domain
      - models
      - rules (deal/contract)
    - services
      - couche applicative
    - cli
      - views/controlleurs (render)
    - utils
