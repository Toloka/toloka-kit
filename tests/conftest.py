import asyncio
import inspect
import pickle
import random
import uuid
from typing import AsyncGenerator

import httpx
import pytest
from pytest_lazyfixture import lazy_fixture
from toloka.async_client import AsyncTolokaClient
from toloka.util.async_utils import isasyncgenadapterfunction
from toloka.client import TolokaClient


class SyncOverAsyncTolokaClient:
    def __init__(self, sync_client, use_async_gen_adapter_as_gen):
        self.async_client = AsyncTolokaClient.from_sync_client(sync_client)
        self.use_async_gen_adapter_as_gen = use_async_gen_adapter_as_gen

    def read_async_gen(self, async_gen):
        loop = asyncio.get_event_loop()
        while True:
            try:
                yield loop.run_until_complete(async_gen.__anext__())
            except StopAsyncIteration:
                return

    def __getattr__(self, name):
        member = getattr(self.async_client, name)
        if (
            inspect.iscoroutinefunction(member)
            or (isasyncgenadapterfunction(member) and not self.use_async_gen_adapter_as_gen)
        ):
            def sync_wrapper(*args, **kwargs):
                value = asyncio.get_event_loop().run_until_complete(member(*args, **kwargs))
                return value
            return sync_wrapper
        if (
            inspect.isasyncgenfunction(member)
            or (isasyncgenadapterfunction(member) and self.use_async_gen_adapter_as_gen)
        ):
            def sync_wrapper(*args, **kwargs):
                yield from self.read_async_gen(member(*args, **kwargs))
            return sync_wrapper

        return member

    def __setattr__(self, key, value):
        if key in ['async_client', 'use_async_gen_adapter_as_gen']:
            object.__setattr__(self, key, value)
        else:
            setattr(self.async_client, key, value)

    def __getstate__(self):
        return self.async_client.__dict__

    def __setstate__(self, state):
        self.async_client = AsyncTolokaClient.__new__(AsyncTolokaClient)
        self.async_client.__dict__ = state


@pytest.fixture
def sync_toloka_client():
    return TolokaClient('fake-token', 'SANDBOX', timeout=0.1, retries=1)


@pytest.fixture
def async_toloka_client():
    return AsyncTolokaClient('fake-token', 'SANDBOX', timeout=0.1, retries=1)


@pytest.fixture(params=[True, False])
def sync_over_async_toloka_client(sync_toloka_client, request):
    return SyncOverAsyncTolokaClient(sync_client=sync_toloka_client, use_async_gen_adapter_as_gen=request.param)


@pytest.fixture(params=[lazy_fixture('sync_toloka_client'), lazy_fixture('sync_over_async_toloka_client')])
def toloka_client(request) -> TolokaClient:
    return request.param


@pytest.fixture
def toloka_client_with_expected_header(toloka_client):
    if isinstance(toloka_client, TolokaClient):
        return toloka_client, 'client'
    return toloka_client, 'async_client'


@pytest.fixture
def sync_toloka_client_prod():
    return TolokaClient('fake-token', 'PRODUCTION')


@pytest.fixture(params=[True, False])
def sync_over_async_toloka_client_prod(sync_toloka_client_prod, request):
    return SyncOverAsyncTolokaClient(sync_toloka_client_prod, use_async_gen_adapter_as_gen=request.param)


@pytest.fixture(params=[lazy_fixture('sync_toloka_client_prod'), lazy_fixture('sync_over_async_toloka_client_prod')])
def toloka_client_prod(request) -> TolokaClient:
    return request.param


@pytest.fixture
def toloka_api_url(toloka_client) -> str:
    return f'{toloka_client.url}/api'


@pytest.fixture
def toloka_url(toloka_api_url) -> str:
    return f'{toloka_api_url}/v1'


@pytest.fixture
def toloka_app_url(toloka_client_prod) -> str:
    return f'{toloka_client_prod.url}/api/app/v0'


@pytest.fixture
def no_uuid_random():
    rd = random.Random()
    rd.seed(0)
    uuid.uuid4 = lambda: uuid.UUID(int=rd.getrandbits(128))
