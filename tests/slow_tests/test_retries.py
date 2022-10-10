import httpx
import pytest
import requests
from urllib3.util import Retry
from toloka.client import TolokaClient
from toloka.async_client import AsyncTolokaClient


def test_socket_timeout_is_retried(timeout_server_url, fake_requester, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    assert toloka_client.get_requester() == fake_requester


@pytest.mark.asyncio
async def test_socket_timeout_is_retried_async(timeout_server_url, fake_requester, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    assert await toloka_client.get_requester() == fake_requester


def test_read_timeout_when_not_retried_enough(timeout_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response - 1, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(httpx.ReadTimeout):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{timeout_server_url}/retries_before_response').text)
    assert retries_left == 0


@pytest.mark.asyncio
async def test_read_timeout_when_not_retried_enough_async(timeout_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response - 1, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(httpx.ReadTimeout):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{timeout_server_url}/retries_before_response').text)
    assert retries_left == 0



def test_retries_off(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=0,
        timeout=0.1
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
        timeout=0.1
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 1


def test_retries_from_int(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=2,
        timeout=0.1
    )

    with pytest.raises(httpx.HTTPStatusError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3


@pytest.mark.asyncio
async def test_retries_from_int_async(connection_error_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=2,
        timeout=0.1
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3



def test_retries_from_class(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=Retry(2, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(httpx.HTTPStatusError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3


@pytest.mark.asyncio
async def test_retries_from_class_async(connection_error_server_url, retries_before_response):
    toloka_client = AsyncTolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=Retry(2, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(httpx.HTTPStatusError):
        await toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3
