import re
import traceback
from inspect import signature

import pytest
from toloka.util._codegen import expand_func_by_argument


@pytest.fixture
def simple_class():
    class Dummy:
        def __init__(self, x: int, y: str = 4):
            if y == 'raise':
                raise ValueError

    return Dummy


def test_expand_function_by_arg(simple_class):
    # TODO: test positional-only
    # TODO: test varargs

    def func(a: bool, b: simple_class, c: simple_class) -> float:
        pass

    # No signature found for builtin type <class 'bool'>
    with pytest.raises(ValueError):
        expand_func_by_argument(func, 'a')

    # ValueError: non-default argument follows default argument
    # (a: bool, x: int, y: str = 4, c: Dummy)
    with pytest.raises(ValueError):
        expand_func_by_argument(func, 'b')

    def expected(a: bool, b: simple_class, x: int, y: str = 4) -> float:
        pass

    assert signature(expected) == signature(expand_func_by_argument(func, 'c'))


def test_generated_source_in_traceback(simple_class):

    def func(a: int, b: simple_class):
        pass

    # Should be equal to
    # def func_expanded_by_b(a: int, x: int, y: str = 4) -> float
    #     b = Dummy(x, y=y)
    #     return func(a, b)
    expanded_func = expand_func_by_argument(func, 'b')

    with pytest.raises(ValueError) as exc_info:
        expanded_func(5, x=0, y='raise')

    trace = ''.join(traceback.format_tb(exc_info.tb))
    pattern = (
        '  File "func_expanded_by_b_\\w+", line 3, in func_expanded_by_b\n'
        '    b = Dummy\\(x, y\\)'
    )
    assert 1 == len(re.findall(pattern, trace))
