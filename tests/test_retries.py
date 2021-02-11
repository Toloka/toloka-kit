import pytest
import requests
import unittest.mock as mock
import urllib3
from urllib3.util.retry import Retry

from toloka.client import TolokaClient


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
        toloka_client = TolokaClient('fake-token', 'SANDBOX', Retry(connect=2))
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 3
