import unittest.mock as mock

import pytest
import requests
import urllib3
from toloka.client import TolokaClient
from urllib3.util import Retry


def urllib_request_mock(self, *args, **kwargs):
    raise urllib3.exceptions.NewConnectionError(self, 'Mocked connection error')


@pytest.mark.xfail(
    reason='TODO: flaky test',
    raises=AssertionError,
)
def test_retries_off():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', 0)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 1


@pytest.mark.xfail(
    reason='TODO: flaky test',
    raises=AssertionError,
)
def test_retries_from_int():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', 1)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 2


@pytest.mark.xfail(
    reason='TODO: flaky test',
    raises=AssertionError,
)
def test_retries_from_class():
    with mock.patch('urllib3.connection.HTTPSConnection.request') as request_mock:
        request_mock.side_effect = urllib_request_mock
        toloka_client = TolokaClient('fake-token', 'SANDBOX', Retry(connect=2), retry_quotas=None)
        with pytest.raises(requests.exceptions.ConnectionError):
            toloka_client.get_requester()
        assert request_mock.call_count == 3
