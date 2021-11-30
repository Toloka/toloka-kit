import pytest
import requests
import sys
from urllib3.util import Retry
from toloka.client import TolokaClient


@pytest.mark.skipif(sys.version_info < (3, 7), reason='aiohttp requires python3.7 or higher')
def test_socket_timeout_is_retried(timeout_server_url, fake_requester, retries_before_response):

    toloka_client = TolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    assert toloka_client.get_requester() == fake_requester


@pytest.mark.skipif(sys.version_info < (3, 7), reason='aiohttp requires python3.7 or higher')
def test_socket_connection_error_when_not_retried_enough(timeout_server_url, retries_before_response):

    toloka_client = TolokaClient(
        'fake-token',
        url=timeout_server_url,
        retries=Retry(retries_before_response - 1, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{timeout_server_url}/retries_before_response').text)
    assert retries_left == 0


@pytest.mark.skipif(sys.version_info < (3, 7), reason='aiohttp requires python3.7 or higher')
def test_retries_off(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=0,
        timeout=0.1
    )

    with pytest.raises(requests.exceptions.RetryError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 1


@pytest.mark.skipif(sys.version_info < (3, 7), reason='aiohttp requires python3.7 or higher')
def test_retries_from_int(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=2,
        timeout=0.1
    )

    with pytest.raises(requests.exceptions.RetryError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3


@pytest.mark.skipif(sys.version_info < (3, 7), reason='aiohttp requires python3.7 or higher')
def test_retries_from_class(connection_error_server_url, retries_before_response):
    toloka_client = TolokaClient(
        'fake-token',
        url=connection_error_server_url,
        retries=Retry(2, status_forcelist={500}, backoff_factor=0),
        retry_quotas=None,
        timeout=0.1
    )

    with pytest.raises(requests.exceptions.RetryError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{connection_error_server_url}/retries_before_response').text)
    assert retries_left == retries_before_response - 3
