import asyncio
import re
import traceback
from functools import partial
from inspect import signature
from io import StringIO

import pytest
from pytest_lazyfixture import lazy_fixture
from toloka.util._codegen import expand_func_by_argument, universal_decorator


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


@pytest.fixture
def universal_logging_decorator():
    buffer = []

    @universal_decorator(has_parameters=False)
    def decorator(func):
        def wrapped(*args, **kwargs):
            buffer.append((args, kwargs))
            return func(*args, **kwargs)

        return wrapped

    return decorator, buffer


@pytest.fixture
def universal_logging_decorator_with_parameters():
    buffer = []

    @universal_decorator(has_parameters=True)
    def decorator(param):
        def wrapper(func):
            def wrapped(*args, **kwargs):
                buffer.append((args, kwargs))
                return func(*args, **kwargs)
            return wrapped
        return wrapper

    return decorator(param=123), buffer


@pytest.mark.parametrize(
    'decorator_with_buffer',
    [lazy_fixture('universal_logging_decorator'), lazy_fixture('universal_logging_decorator_with_parameters')]
)
def test_universal_decorator_plain_function(decorator_with_buffer):
    decorator, buffer = decorator_with_buffer

    @decorator
    def func(a, b=None):
        return a, b

    assert func(10, b=20) == (10, 20)
    assert func(10, 20) == (10, 20)
    assert func(10) == (10, None)
    assert buffer == [((10,), {'b': 20}), ((10, 20), {}), ((10,), {})]


@pytest.mark.parametrize(
    'decorator_with_buffer',
    [lazy_fixture('universal_logging_decorator'), lazy_fixture('universal_logging_decorator_with_parameters')]
)
def test_universal_decorator_generator(decorator_with_buffer):
    decorator, buffer = decorator_with_buffer

    @decorator
    def func(a, b=None):
        yield a, b

    assert list(func(10, b=20)) == [(10, 20)]
    assert list(func(10, 20)) == [(10, 20)]
    assert list(func(10)) == [(10, None)]
    assert buffer == [((10,), {'b': 20}), ((10, 20), {}), ((10,), {})]


@pytest.mark.parametrize(
    'decorator_with_buffer',
    [lazy_fixture('universal_logging_decorator'), lazy_fixture('universal_logging_decorator_with_parameters')]
)
def test_universal_decorator_async(decorator_with_buffer):
    decorator, buffer = decorator_with_buffer

    @decorator
    async def func(a, b=None):
        return a, b

    assert asyncio.run(func(10, b=20)) == (10, 20)
    assert asyncio.run(func(10, 20)) == (10, 20)
    assert asyncio.run(func(10)) == (10, None)
    assert buffer == [((10,), {'b': 20}), ((10, 20), {}), ((10,), {})]


@pytest.mark.parametrize(
    'decorator_with_buffer',
    [lazy_fixture('universal_logging_decorator'), lazy_fixture('universal_logging_decorator_with_parameters')]
)
def test_universal_decorator_async_generator(decorator_with_buffer):
    decorator, buffer = decorator_with_buffer

    @decorator
    async def func(a, b=None):
        yield a, b

    async def collect_async_gen(*args, **kwargs):
        return [item async for item in func(*args, **kwargs)]

    assert asyncio.run(collect_async_gen(10, b=20)) == [(10, 20)]
    assert asyncio.run(collect_async_gen(10, 20)) == [(10, 20)]
    assert asyncio.run(collect_async_gen(10)) == [(10, None)]
    assert buffer == [((10,), {'b': 20}), ((10, 20), {}), ((10,), {})]
