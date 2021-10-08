import pathlib
import re
import shutil
from typing import Any, Pattern

import nox

nox.options.reuse_existing_virtualenvs = True
python_versions = ("3.7.12", "3.8.12", "3.9.7")
numpy_versions = ("1.17.5", "1.18.5", "1.19.5", "1.20.3", "1.21.2")
exclude = (("3.9.7", "1.18.5"),)
matrix = tuple(
    (python, numpy)
    for python in python_versions
    for numpy in numpy_versions
    if (python, numpy) not in exclude
    )
ids = tuple(
    f"{python}/{numpy}"
    for python, numpy in matrix
    )


class SessionCache:
    sesh_name: str
    sesh_cache: str
    pattern: Pattern = re.compile(r"\(|\)|\/|\=|\'|\"|\,|\s")

    def __init__(self, sesh_name: str, sesh_cache: str) -> None:
        self.lock_name = self.pattern.sub("-", sesh_name)
        self.back_lock = pathlib.Path(f"{sesh_cache}/poetry.lock")
        self.back_toml = pathlib.Path(f"{sesh_cache}/pyproject.toml")
        self.base_lock = pathlib.Path("poetry.lock")
        self.base_toml = pathlib.Path("pyproject.toml")
        self.sesh_lock = pathlib.Path(f"{sesh_cache}/lock-{self.lock_name}")

        if not self.sesh_lock.exists():
            shutil.copyfile(self.base_lock, self.sesh_lock)

    def __enter__(self) -> None:
        shutil.copyfile(self.base_lock, self.back_lock)
        shutil.copyfile(self.base_toml, self.back_toml)
        shutil.copyfile(self.sesh_lock, self.base_lock)

    def __exit__(self, *__: Any) -> None:
        shutil.copyfile(self.base_lock, self.sesh_lock)
        shutil.copyfile(self.back_lock, self.base_lock)
        shutil.copyfile(self.back_toml, self.base_toml)
        self.back_lock.unlink()
        self.back_toml.unlink()


@nox.session
@nox.parametrize("python, numpy", matrix, ids = ids)
def test(session, numpy):
    session.run("make", "install", external = True, silent = True)

    with SessionCache(session.name, session.cache_dir):
        session.run("poetry", "add", f"numpy@{numpy}", silent = True)
        session.run("poetry", "install", silent = True)

    session.run("poetry", "run", "pytest", "-qx")
