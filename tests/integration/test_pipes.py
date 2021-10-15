import deal

from pysemver import utils


def function_decorator(function):
    return function


class class_decorator:
    def __call__(_self, function):
        return function


def test_pipes_with_function_decorator():
    @function_decorator
    @utils.pipes
    def function(*ints: int) -> str:
        return ints >> sum << str

    assert function(1, 2, 3) == "6"


def test_pipes_with_class_decorator():
    @class_decorator()
    @utils.pipes
    def function(*ints: int) -> str:
        return ints >> sum << str

    assert function(1, 2, 3) == "6"


def test_pipes_with_deal():
    @deal.has()
    @utils.pipes
    def function(*ints: int) -> str:
        return ints >> sum << str

    assert function(1, 2, 3) == "6"
