# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

import inspect

import pytest
from numpy.testing import assert_equal

from pysemver._builder import SignatureBuilder
from pysemver.services.signatures import CheckSignature, diff_hash

from . import fixtures


@pytest.fixture
def this_builder():
    return SignatureBuilder(["file.py"])


@pytest.fixture
def that_builder():
    return SignatureBuilder(["file.py"])


def test(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [0, 0, 0, 0])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 0, 0, 0])
    assert_equal(checker.diff_type(), [0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0])
    assert checker.score() == 0
    assert checker.reason is None


def test_when_added_args(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_more_args))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1, 1, 1])
    assert_equal(checker.diff_args(), [2, 2, 2, 2, 2, 2])
    assert_equal(checker.diff_name(), [0, 0, 0, 0, 2, 2])
    assert_equal(checker.diff_type(), [0, 0, 0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0, 3, 3])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_removed_args(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_more_args))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1, 1, 1])
    assert_equal(checker.diff_args(), [3, 3, 3, 3, 3, 3])
    assert_equal(checker.diff_name(), [0, 0, 0, 0, 2, 2])
    assert_equal(checker.diff_type(), [0, 0, 0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0, 2, 2])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_changed_arg_names(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_changed_args))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 3, 3, 0])
    assert_equal(checker.diff_type(), [0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_added_types(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_types))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 0, 0, 0])
    assert_equal(checker.diff_type(), [1, 1, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0])
    assert checker.score() == 1
    assert checker.reason == "types-diff"


def test_when_removed_types(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_types))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 0, 0, 0])
    assert_equal(checker.diff_type(), [1, 1, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0])
    assert checker.score() == 1
    assert checker.reason == "types-diff"


def test_when_added_defaults(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_defaults))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 0, 0, 0])
    assert_equal(checker.diff_type(), [0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 2, 2])
    assert checker.score() == 2
    assert checker.reason == "defaults-diff"


def test_when_removed_defaults(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_defaults))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1])
    assert_equal(checker.diff_args(), [0, 0, 0, 0])
    assert_equal(checker.diff_name(), [0, 0, 0, 0])
    assert_equal(checker.diff_type(), [0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 3, 3])
    assert checker.score() == 3
    assert checker.reason == "defaults-diff"


def test_when_added_args_and_defs(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_more_defaults))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1, 1, 1])
    assert_equal(checker.diff_args(), [2, 2, 2, 2, 2, 2])
    assert_equal(checker.diff_name(), [0, 0, 0, 0, 2, 2])
    assert_equal(checker.diff_type(), [0, 0, 0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0, 0, 0])
    assert checker.score() == 2
    assert checker.reason == "args/defaults-diff"


def test_when_removed_args_and_defs(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_more_defaults))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker), [1, 1, 1, 1, 1, 1])
    assert_equal(checker.diff_args(), [3, 3, 3, 3, 3, 3])
    assert_equal(checker.diff_name(), [0, 0, 0, 0, 2, 2])
    assert_equal(checker.diff_type(), [0, 0, 0, 0, 0, 0])
    assert_equal(checker.diff_defs(), [0, 0, 0, 0, 0, 0])
    assert checker.score() == 3
    assert checker.reason == "args-diff"
