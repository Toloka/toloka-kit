import pytest
import requests
from toloka.client import TolokaClient


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
