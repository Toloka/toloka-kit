import asyncio
import functools
from concurrent import futures
import contextvars
import pytest

from toloka.util._managing_headers import (
    add_headers,
    async_add_headers,
    form_additional_headers,
)


def test_simple_function():

    @add_headers('TestClient')
    def get_additional_headers():
        return form_additional_headers()

    assert get_additional_headers() == {
        'X-Caller-Context': 'TestClient',
        'X-Top-Level-Method': 'get_additional_headers',
        'X-Low-Level-Method': 'get_additional_headers',
    }


def test_complex_function():

    @add_headers('TestClient')
    def get_additional_headers():
        return form_additional_headers()

    @add_headers('AnotherTestClient')
    def complex_func():
        return get_additional_headers()

    additional_headers = complex_func()
    assert additional_headers == {
        'X-Caller-Context': 'AnotherTestClient',
        'X-Top-Level-Method': 'complex_func',
        'X-Low-Level-Method': 'get_additional_headers',
    }


@pytest.mark.asyncio
async def test_async_simple_function():

    @async_add_headers('TestClient')
    async def async_get_additional_headers():
        return form_additional_headers()

    additional_headers = await async_get_additional_headers()

    assert additional_headers == {
        'X-Caller-Context': 'TestClient',
        'X-Top-Level-Method': 'async_get_additional_headers',
        'X-Low-Level-Method': 'async_get_additional_headers',
    }


@pytest.mark.asyncio
async def test_async_complex_function():

    @async_add_headers('TestClient')
    async def async_get_additional_headers():
        return form_additional_headers()

    @async_add_headers('AsyncTestClient')
    async def async_complex_func():
        return await async_get_additional_headers()

    additional_headers = await async_complex_func()

    assert additional_headers == {
        'X-Caller-Context': 'AsyncTestClient',
        'X-Top-Level-Method': 'async_complex_func',
        'X-Low-Level-Method': 'async_get_additional_headers',
    }


@pytest.mark.parametrize('n', [10])
def test_generator(n):

    @add_headers('TestClient')
    def get_additional_headers():
        return form_additional_headers()

    def generator_with_context(func, number_of_generations):
        # It is important to capture context
        ctx = contextvars.copy_context()
        yield
        for _ in range(number_of_generations):
            yield ctx.run(func)

    @add_headers('GeneratorClient')
    def with_generator_client_context(func, number_of_generations):
        generator = generator_with_context(func, number_of_generations)
        # It is important to "activate" generator to capture context
        generator.send(None)
        return generator

    for additional_headers in with_generator_client_context(get_additional_headers, n):
        assert additional_headers == {
            'X-Caller-Context': 'GeneratorClient',
            'X-Top-Level-Method': 'with_generator_client_context',
            'X-Low-Level-Method': 'get_additional_headers',
        }

    for additional_headers in (get_additional_headers() for _ in range(n)):
        assert additional_headers == {
            'X-Caller-Context': 'TestClient',
            'X-Top-Level-Method': 'get_additional_headers',
            'X-Low-Level-Method': 'get_additional_headers',
        }


@pytest.mark.parametrize('n', [1])
@pytest.mark.asyncio
async def test_async_generator(n):

    @add_headers('TestClient')
    def get_additional_headers():
        return form_additional_headers()

    async def generator_with_context(func, number_of_generations):
        # It is important to capture context
        ctx = contextvars.copy_context()
        yield
        for _ in range(number_of_generations):
            yield ctx.run(func)

    @async_add_headers('GeneratorClient')
    async def with_async_generator_client_context(func, number_of_generations):
        generator = generator_with_context(func, number_of_generations)
        # It is important to "activate" generator to capture context
        await generator.asend(None)
        return generator

    async for additional_headers in await with_async_generator_client_context(get_additional_headers, n):
        assert additional_headers == {
            'X-Caller-Context': 'GeneratorClient',
            'X-Top-Level-Method': 'with_async_generator_client_context',
            'X-Low-Level-Method': 'get_additional_headers',
        }

    for additional_headers in (get_additional_headers() for _ in range(n)):
        assert additional_headers == {
            'X-Caller-Context': 'TestClient',
            'X-Top-Level-Method': 'get_additional_headers',
            'X-Low-Level-Method': 'get_additional_headers',
        }


@pytest.mark.parametrize('executor', [futures.ProcessPoolExecutor(max_workers=5),
                         futures.ThreadPoolExecutor(max_workers=5)])
@pytest.mark.asyncio
async def test_run_in_pool_executor(executor):

    def func_with_init_vars(*args, **kwargs):
        # func and ctx_vars are not separate arguments because of possibility them to be in kwargs as func args
        # TODO in python >=3.8 it could be fixed by "def func_with_init_vars(func, ctx_vars, *args, /, **kwargs)"
        func, ctx_vars, *args_for_func = args
        for var, value in ctx_vars.items():
            var.set(value)
        return func(*args_for_func, **kwargs)

    @async_add_headers('streaming')
    async def async_wrapper(func):
        loop = asyncio.get_event_loop()
        ctx = contextvars.copy_context()

        return await loop.run_in_executor(
            executor,
            functools.partial(func_with_init_vars, func, ctx, ctx='fake_argument')
        )

    @add_headers('client')
    def get_additional_headers(**kwargs):
        return form_additional_headers()

    if isinstance(executor, futures.ThreadPoolExecutor):
        additional_headers = await async_wrapper(get_additional_headers)

        assert additional_headers == {
            'X-Caller-Context': 'streaming',
            'X-Top-Level-Method': 'async_wrapper',
            'X-Low-Level-Method': 'get_additional_headers',
        }
    elif isinstance(executor, futures.ProcessPoolExecutor):
        # Context objects not picklable, so it can't be used in ProcessPoolExecutor (check PEP 567)
        with pytest.raises(Exception):
            await async_wrapper(get_additional_headers)
