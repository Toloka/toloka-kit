import asyncio
import json
import pytest
import random
import requests
import time
import uuid

from aiohttp import web
from aiohttp.test_utils import unused_port
from copy import copy
from decimal import Decimal
from multiprocessing import Process
from toloka.client import TolokaClient
from toloka.client.requester import Requester


@pytest.fixture
def toloka_client() -> TolokaClient:
    return TolokaClient('fake-token', 'SANDBOX')


@pytest.fixture
def toloka_client_prod() -> TolokaClient:
    return TolokaClient('fake-token', 'PRODUCTION')


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


# local test requester server


@pytest.fixture(scope='session')
def fake_requester():
    return Requester(id='123', balance=Decimal(1000000.0000), public_name={'EN': 'fake'})


class RetryCountingHandler:
    def __init__(self, retries_before_response, requester):
        self.retries_before_response = retries_before_response
        self.retries_left = retries_before_response
        self.requester = copy(requester)
        self.requester.balance = float(self.requester.balance)

    async def get_requester(self, request):
        response = web.StreamResponse()
        response.content_type = 'application/json'
        response.enable_chunked_encoding()
        await response.prepare(request)
        self.retries_left -= 1
        if self.retries_left >= 0:
            await asyncio.sleep(10)
        await response.write(json.dumps(self.requester.unstructure()).encode('utf-8'))
        return response

    async def get_retries_before_response(self, request):
        return web.Response(text=str(self.retries_left))

    async def reset_server(self, request):
        self.retries_left = self.retries_before_response
        return web.Response(text='OK')

    async def ping(self, request):
        return web.Response(text='OK')


@pytest.fixture(scope='session')
def server_port():
    try:
        from yatest.common.network import PortManager
        with PortManager() as port_manager:
            yield port_manager.get_port()

    except ImportError:
        yield unused_port()


@pytest.fixture(scope='session')
def server_url():
    return 'localhost'


def run_server(app, url, port):
    web.run_app(app, host=url, port=port)


@pytest.fixture(scope='session')
def sleepy_server(server_url, server_port, fake_requester):
    app = web.Application()
    retries_before_response = 10
    handler = RetryCountingHandler(retries_before_response, fake_requester)
    app.add_routes([
        web.get('/api/v1/requester', handler.get_requester),
        web.get('/ping', handler.ping),
        web.get('/retries_before_response', handler.get_retries_before_response),
        web.get('/reset', handler.reset_server),
    ])

    server_process = Process(target=run_server, args=(app, server_url, server_port))
    server_process.daemon = True
    server_process.start()

    url = f'http://{server_url}:{server_port}'

    for _ in range(30):
        try:
            if requests.get(f'{url}/ping', timeout=0.1).status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass

        print('Server is not started... sleeping for 1s')
        time.sleep(1)
    else:
        raise RuntimeError("Can't start server")
    yield url, retries_before_response


@pytest.fixture()
def reset_sleepy_server(sleepy_server):
    url, _ = sleepy_server
    requests.get(f'{url}/reset')
    return sleepy_server
