import asyncio
import json
import sys
import time
from copy import copy
from decimal import Decimal
from multiprocessing import Process

import pytest
import requests
from toloka.client.requester import Requester

if sys.version_info >= (3, 7):
    from aiohttp import web
    from aiohttp.test_utils import unused_port


# local test requester server

@pytest.fixture(scope='session')
def fake_requester():
    return Requester(id='123', balance=Decimal(1000000.0000), public_name={'EN': 'fake'})


@pytest.fixture(scope='session')
def retries_before_response():
    return 10


class RetryCountingHandler:
    def __init__(self, retries_before_response, requester):
        self.retries_left = retries_before_response
        self.requester = copy(requester)
        self.requester.balance = float(self.requester.balance)
        self.streaming_mode = True

    async def get_requester(self, request):
        if self.streaming_mode:
            response = web.StreamResponse()
            response.content_type = 'application/json'
            response.enable_chunked_encoding()
            await response.prepare(request)
            self.retries_left -= 1
            if self.retries_left >= 0:
                await asyncio.sleep(10)
            await response.write(json.dumps(self.requester.unstructure()).encode('utf-8'))
            return response
        else:
            self.retries_left -= 1
            if self.retries_left >= 0:
                return web.Response(status=500)
            return web.Response(
                content_type='application/json',
                body=json.dumps(self.requester.unstructure())
            )

    async def get_retries_before_response(self, request):
        return web.Response(text=str(self.retries_left))

    async def reset_server(self, request):
        reset_params = await request.json()
        self.retries_left = int(reset_params['retries'])
        self.streaming_mode = bool(reset_params['streaming_mode'])

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
def launched_test_server_url(server_url, server_port, fake_requester, retries_before_response):
    app = web.Application()
    handler = RetryCountingHandler(retries_before_response, fake_requester)
    app.add_routes([
        web.get('/api/v1/requester', handler.get_requester),
        web.get('/ping', handler.ping),
        web.get('/retries_before_response', handler.get_retries_before_response),
        web.post('/reset', handler.reset_server),
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
    yield url


@pytest.fixture
def timeout_server_url(launched_test_server_url, retries_before_response):
    requests.post(f'{launched_test_server_url}/reset', json={
        'retries': retries_before_response,
        'streaming_mode': True,
    })
    return launched_test_server_url


@pytest.fixture
def connection_error_server_url(launched_test_server_url, retries_before_response):
    requests.post(f'{launched_test_server_url}/reset', json={
        'retries': retries_before_response,
        'streaming_mode': False,
    })
    return launched_test_server_url
