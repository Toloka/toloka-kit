import logging
import socket
from threading import Thread

import httpx
import pytest
import requests
from aiohttp.test_utils import unused_port
from toloka.async_client import AsyncTolokaClient
from toloka.client import TolokaClient
from urllib3.util import Retry

logger = logging.getLogger(__file__)


class ConnectionCounter:
    def __init__(self):
        self.connections_count = 0

    def increment(self):
        self.connections_count += 1


def create_requester_socket_timeout_server(
    server_socket, retries_before_response, requester, accepted_connections_counter: ConnectionCounter
):
    try:
        seen_connections = []
        # hangs connection without closing it retries_before_response times
        for i in range(retries_before_response):
            accepted_socket, accepted_address = server_socket.accept()
            # reference socket to prevent closing it by garbage collector
            seen_connections.append(accepted_socket)
            accepted_connections_counter.increment()

        conn, client_address = server_socket.accept()
        accepted_connections_counter.increment()
        conn.recv(1024).decode()
        conn.sendall(
            f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{requester.to_json()}'.encode()
        )
        conn.close()
    except Exception as exc:
        logger.error(exc)


def create_requester_socket_timeout_middle_connection_server(
    server_socket, retries_before_response, requester, accepted_connections_counter: ConnectionCounter
):
    response_body = requester.to_json()

    try:
        seen_connections = []
        # sends part of response and hangs connection without closing it retries_before_response times
        for i in range(retries_before_response):
            accepted_socket, accepted_address = server_socket.accept()
            accepted_socket.sendall(
                f'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\nContent-Type: application/json\r\n\r\n'.encode()
            )
            accepted_socket.sendall(
                f'{"%X" % len(response_body[:10])}\r\n{response_body[:10]}\r\n'.encode()
            )
            # reference socket to prevent closing it by garbage collector
            seen_connections.append(accepted_socket)
            accepted_connections_counter.increment()

        conn, client_address = server_socket.accept()
        accepted_connections_counter.increment()
        conn.recv(1024).decode()
        conn.sendall(
            f'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\nContent-Type: application/json\r\n\r\n'.encode()
        )
        conn.sendall(
            f'{"%X" % len(response_body[:10])}\r\n{response_body[:10]}\r\n'.encode()
        )
        conn.sendall(
            f'{"%X" % len(response_body[10:])}\r\n{response_body[10:]}\r\n'.encode()
        )
        conn.sendall(
            '0\r\n\r\n'.encode()
        )
        conn.close()
    except Exception as exc:
        logger.error(exc)


@pytest.fixture(params=[
    create_requester_socket_timeout_server,
    create_requester_socket_timeout_middle_connection_server
])
def requester_socket_timeout_server(request, retries_before_response, fake_requester):
    address = ('localhost', unused_port())

    # in python3.8+ socket.create_server can be used
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if socket.has_ipv6:
        server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    server_socket.bind(address)
    server_socket.listen(100)

    connection_counter = ConnectionCounter()
    t = Thread(
        target=request.param,
        args=(server_socket, retries_before_response, fake_requester, connection_counter),
        daemon=True,
    )
    t.start()
    return f'http://localhost:{address[1]}', connection_counter


def test_socket_timeout_is_retried(requester_socket_timeout_server, fake_requester, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=requester_socket_timeout_server[0],
        retries=Retry(retries_before_response, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )
    assert toloka_client.get_requester() == fake_requester


@pytest.mark.asyncio
async def test_socket_timeout_is_retried_async(
    requester_socket_timeout_server, fake_requester, retries_before_response
):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=requester_socket_timeout_server[0],
        retries=Retry(retries_before_response, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    assert await toloka_client.get_requester() == fake_requester


def test_read_timeout_when_not_retried_enough(
    requester_socket_timeout_server, fake_requester, retries_before_response
):
    toloka_client = TolokaClient(
        'fake-token',
        url=requester_socket_timeout_server[0],
        retries=Retry(retries_before_response - 1, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    with pytest.raises(httpx.ReadTimeout):
        toloka_client.get_requester()

    assert requester_socket_timeout_server[1].connections_count == retries_before_response


@pytest.mark.asyncio
async def test_read_timeout_when_not_retried_enough_async(
    requester_socket_timeout_server, retries_before_response
):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=requester_socket_timeout_server[0],
        retries=Retry(retries_before_response - 1, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    with pytest.raises(httpx.ReadTimeout):
        await toloka_client.get_requester()

    assert requester_socket_timeout_server[1].connections_count == retries_before_response


def test_retries_off(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=0,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 1


@pytest.mark.asyncio
async def test_retries_off_async(connection_error_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=0,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 1


def test_retries_from_int(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=retries_before_response - 1,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == 0


@pytest.mark.asyncio
async def test_retries_from_int_async(connection_error_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=retries_before_response - 1,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == 0


def test_retries_from_class(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=Retry(retries_before_response - 1, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == 0


@pytest.mark.asyncio
async def test_retries_from_class_async(connection_error_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=Retry(retries_before_response - 1, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.5,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == 0
