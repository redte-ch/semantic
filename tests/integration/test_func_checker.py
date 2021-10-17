# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

import inspect

import pytest
from numpy.testing import assert_equal

from pysemver.actions import BuildSignatures
from pysemver.actions.check_signature import (
    CheckSignature,
    diff_args,
    diff_defs,
    diff_hash,
    diff_name,
    )
from tests import fixtures


@pytest.fixture
def this_builder():
    return BuildSignatures(["file.py"])


@pytest.fixture
def that_builder():
    return BuildSignatures(["file.py"])


def test(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0])
    assert checker.score() == 0
    assert checker.reason is None


def test_when_added_args(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_more_args))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [2, 2, 2, 2, 2, 2])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0, 2, 2])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0, 3, 3])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_removed_args(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_more_args))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [3, 3, 3, 3, 3, 3])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0, 2, 2])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0, 2, 2])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_changed_arg_names(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_changed_args))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 3, 3, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0])
    assert checker.score() == 3
    assert checker.reason == "args-diff"


def test_when_addedtypes(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_withtypes))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0])
    assert checker.score() == 1
    assert checker.reason == "types-diff"


def test_when_removedtypes(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_withtypes))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0])
    assert checker.score() == 1
    assert checker.reason == "types-diff"


def test_when_added_defaults(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_defaults))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 2, 2])
    assert checker.score() == 2
    assert checker.reason == "defaults-diff"


def test_when_removed_defaults(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_defaults))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 3, 3])
    assert checker.score() == 3
    assert checker.reason == "defaults-diff"


def test_when_added_args_and_defs(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func_with_more_defaults))
    that_builder(inspect.getsource(fixtures.func))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [2, 2, 2, 2, 2, 2])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0, 2, 2])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0, 0, 0])
    assert checker.score() == 2
    assert checker.reason == "args/defaults-diff"


def test_when_removed_args_and_defs(this_builder, that_builder):

    this_builder(inspect.getsource(fixtures.func))
    that_builder(inspect.getsource(fixtures.func_with_more_defaults))

    this, = this_builder.signatures
    that, = that_builder.signatures

    checker = CheckSignature(this, that)

    assert_equal(diff_hash(checker.this, checker.that), [1, 1, 1, 1, 1, 1])
    assert_equal(diff_args(checker.this, checker.that), [3, 3, 3, 3, 3, 3])
    assert_equal(diff_name(checker.this, checker.that), [0, 0, 0, 0, 2, 2])
    assert_equal(diff_defs(checker.this, checker.that), [0, 0, 0, 0, 0, 0])
    assert checker.score() == 3
    assert checker.reason == "args-diff"
