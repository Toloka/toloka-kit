import unittest.mock as mock

import pytest
import requests
import urllib3
from toloka.client import TolokaClient
from urllib3.util import Retry


def urllib_request_mock(self, *args, **kwargs):
    raise urllib3.exceptions.NewConnectionError(self, 'Mocked connection error')


def test_retries_off():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', 0)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 1


def test_retries_from_int():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', 1)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 2


def test_retries_from_class():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', Retry(connect=2), retry_quotas=None)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 3


@pytest.mark.xfail(
    reason='Timeout errors during content read are not retried with urllib.utils.Retry and requests',
    raises=requests.exceptions.ConnectionError,
)
def test_socket_timeout_is_retried(reset_sleepy_server, server_port, server_url, fake_requester):
    sleepy_server_url, retries_before_response = reset_sleepy_server

    toloka_client = TolokaClient(
        'fake-token',
        url=sleepy_server_url,
        retries=retries_before_response,
        timeout=0.1
    )

    assert toloka_client.get_requester() == fake_requester


@pytest.mark.xfail(
    reason='Timeout errors during content read are not retried with urllib.utils.Retry and requests',
    raises=AssertionError,
)
def test_socket_connection_error_when_not_retried_enough(reset_sleepy_server, server_port, server_url, fake_requester):
    sleepy_server_url, retries_before_response = reset_sleepy_server

    toloka_client = TolokaClient(
        'fake-token',
        url=sleepy_server_url,
        retries=retries_before_response - 1,
        timeout=0.1
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        toloka_client.get_requester()

    retries_left = int(requests.get(f'{sleepy_server_url}/retries_before_response').text)
    assert retries_left == 1
