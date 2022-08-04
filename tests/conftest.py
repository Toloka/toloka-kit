import asyncio
import inspect
import random
import uuid

import httpx
import pytest
from pytest_lazyfixture import lazy_fixture
from toloka.async_client import AsyncTolokaClient
from toloka.client import TolokaClient


@pytest.fixture
def sync_toloka_client():
    return TolokaClient('fake-token', 'SANDBOX')


class SyncOverAsyncTolokaClient:
    def __init__(self, sync_client):
        self.async_client = AsyncTolokaClient.from_sync_client(sync_client)

    def __getattr__(self, name):
        member = getattr(self.async_client, name)
        if inspect.iscoroutinefunction(member):
            def sync_wrapper(*args, **kwargs):
                return asyncio.get_event_loop().run_until_complete(member(*args, **kwargs))

            return sync_wrapper
        return member


@pytest.fixture
def sync_over_async_toloka_client(sync_toloka_client):
    return SyncOverAsyncTolokaClient(sync_toloka_client)


@pytest.fixture(params=[lazy_fixture('sync_toloka_client'), lazy_fixture('sync_over_async_toloka_client')])
def toloka_client(request) -> TolokaClient:
    return request.param


@pytest.fixture
def toloka_client_with_expected_header(toloka_client):
    if isinstance(toloka_client, TolokaClient):
        return toloka_client, 'client'
    return toloka_client, 'async_client'


@pytest.fixture
def async_toloka_client():
    return AsyncTolokaClient('fake-token', 'SANDBOX')


@pytest.fixture
def sync_toloka_client_prod():
    return TolokaClient('fake-token', 'PRODUCTION')


@pytest.fixture
def sync_over_async_toloka_client_prod(sync_toloka_client_prod):
    return SyncOverAsyncTolokaClient(sync_toloka_client_prod)


@pytest.fixture(params=[lazy_fixture('sync_toloka_client_prod'), lazy_fixture('sync_over_async_toloka_client_prod')])
def toloka_client_prod(request) -> TolokaClient:
    return request.param


@pytest.fixture
def toloka_client_prod_with_expected_header(toloka_client_prod):
    if isinstance(toloka_client, TolokaClient):
        return toloka_client, 'client'
    return toloka_client, 'async_client'


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


class UniversalRequestsMock:
    def __init__(self, respx_mock, requests_mock):
        self.respx_mock = respx_mock
        self.requests_mock = requests_mock

    def _get_httpx_response(self, json, text, status_code):
        def response(request, route):
            return httpx.Response(status_code, json=json and json(request, route), text=text and text(request, route))

        return response

    def get(self, url, json=None, text=None, status_code=200):
        self.respx_mock.get(url).mock(side_effect=self._get_httpx_response(json, text, status_code))
        self.requests_mock.get(url, json=json, text=text)

    def post(self, url, json=None, text=None, status_code=200):
        self.respx_mock.post(url).mock(side_effect=self._get_httpx_response(json, text, status_code))
        self.requests_mock.post(url, json=json, text=text)

    def patch(self, url, json=None, text=None, status_code=200):
        self.respx_mock.patch(url).mock(side_effect=self._get_httpx_response(json, text, status_code))
        self.requests_mock.patch(url, json=json, text=text)


@pytest.fixture
def universal_requests_mock(respx_mock, requests_mock):
    return UniversalRequestsMock(respx_mock, requests_mock)

