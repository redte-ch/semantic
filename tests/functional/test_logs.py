# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import re

import pytest

from mantic import infra

_colors = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


@pytest.fixture
def capture(capsys):
    """Capture prints."""

    def _capture():
        # We strip colors to test just content.
        return _colors.sub("", capsys.readouterr().out)

    return _capture


def test_init(capture):
    infra.logs.init()
    output = "[/] 0%   |··················································|\r"
    assert capture() == output


def test_push(capture):
    infra.logs.push(0, 2)
    output = "[/] 50%  |✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓·························|\r"
    assert capture() == output


def test_okay(capture):
    infra.logs.okay("Hello!")
    output = "[✓] Hello!"
    assert capture() == output


def test_info(capture):
    infra.logs.info("Hello!")
    output = "[i] Hello!"
    assert capture() == output


def test_warn(capture):
    infra.logs.warn("Hello!")
    output = "[!] Hello!"
    assert capture() == output


def test_fail(capture):
    infra.logs.fail()
    output = "\r[x]"
    assert capture() == output


def test_then(capture):
    infra.logs.then()
    output = "\n\r"
    assert capture() == output


def test_wipe(capture):
    infra.logs.wipe()
    output = "                                                             \r"
    assert capture()[-62:] == output
