import os
import pathlib
import shutil
import tempfile

import nox

nox.options.reuse_existing_virtualenvs = True
py_versions = ["3.7.11", "3.8.12", "3.9.7", "3.10.0"]
np_versions = ["1.18.5", "1.19.5", "1.20.3", "1.21.2"]


@nox.session(python = py_versions)
@nox.parametrize("numpy", np_versions, ids = np_versions)
def test(session, numpy):
    with tempfile.TemporaryDirectory() as test_dir:
        base_dir = pathlib.Path(os.path.abspath("."))
        shutil.rmtree(test_dir)
        shutil.copytree(base_dir, test_dir)
        session.chdir(test_dir)
        session.install("poetry")
        session.run("poetry", "add", f"numpy@{numpy}")
        session.run("poetry", "install")
        session.run("poetry", "run", "pytest", "-qx")
