from typing import Dict

import httpx
import pytest
import tenacity
from httpx._types import URLTypes
from toloka.client.exceptions import ApiError
from toloka.client.primitives.retry import SyncRetryingOverURLLibRetry
from urllib3 import Retry


class ExceptionRaisingRequester:
    def __init__(self, exception):
        self.exception = exception

    def __call__(self, method: str, url: URLTypes, **kwargs):
        raise self.exception


@pytest.mark.parametrize(
    'exception_to_raise', [
        httpx.TimeoutException(''),
        httpx.ConnectTimeout(''),
        httpx.ReadTimeout(''),
        httpx.WriteTimeout(''),
        httpx.ConnectError(''),
        httpx.ReadError(''),
        httpx.WriteError(''),
        httpx.CloseError(''),
        httpx.ProtocolError(''),
        httpx.LocalProtocolError(''),
        httpx.RemoteProtocolError(''),
    ]
)
def test_retrying_retries_relevant_exceptions(exception_to_raise):
    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, total=3),
        reraise=True,
    )
    retrying_request = retrying.wraps(ExceptionRaisingRequester(exception_to_raise))

    with pytest.raises(type(exception_to_raise)):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 4


@pytest.mark.parametrize(
    'exception_to_raise', [
        httpx.NetworkError(''),  # not raised in httpcore, just a base class
        httpx.PoolTimeout(''),
        ValueError(),
    ]
)
def test_retrying_does_not_retry_irrelevant_exceptions(exception_to_raise):
    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, total=3),
        reraise=True,
    )
    retrying_request = retrying.wraps(ExceptionRaisingRequester(exception_to_raise))

    with pytest.raises(type(exception_to_raise)):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 1


@pytest.mark.timeout(1)
def test_raise_for_status_is_retried(respx_mock):
    respx_mock.get(url__regex=r'.*').mock(return_value=httpx.Response(status_code=500))

    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, total=None, status=3, status_forcelist={500}),
        reraise=True,
    )

    def request_with_raise_for_status(method, url, **kwargs):
        response = httpx.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    retrying_request = retrying.wraps(request_with_raise_for_status)

    with pytest.raises(httpx.HTTPStatusError):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 4


@pytest.mark.timeout(1)
def test_raise_for_status_custom_is_retried(respx_mock):
    respx_mock.get(url__regex=r'.*').mock(return_value=httpx.Response(status_code=500))

    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, total=None, status=3, status_forcelist={500}),
        reraise=True,
    )

    def request_with_raise_for_status(method, url, **kwargs):
        response = httpx.request(method, url, **kwargs)
        raise ApiError(status_code=response.status_code, response=response)

    retrying_request = retrying.wraps(request_with_raise_for_status)

    with pytest.raises(ApiError):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 4


@pytest.mark.parametrize(
    'exception_to_raise,retry_kwargs', [
        (httpx.ConnectTimeout(''), {'total': None, 'connect': 3}),
        (httpx.ReadTimeout(''), {'total': None, 'read': 3}),
        (httpx.ReadError(''), {'total': None, 'read': 3}),
        (httpx.RemoteProtocolError(''), {'total': None, 'read': 3}),
    ]
)
@pytest.mark.timeout(1)
def test_retrying_follows_urllib_exception_retrying_quota(exception_to_raise: Exception, retry_kwargs: Dict):
    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, **retry_kwargs),
        reraise=True,
    )
    retrying_request = retrying.wraps(ExceptionRaisingRequester(exception_to_raise))

    with pytest.raises(type(exception_to_raise)):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 4


@pytest.mark.timeout(1)
def test_retrying_follows_urllib_status_retrying_quota(respx_mock):
    respx_mock.get(url__regex=r'.*').mock(
        return_value=httpx.Response(status_code=500)
    )

    retrying = SyncRetryingOverURLLibRetry(
        base_url='http://example.com',
        retry=Retry(backoff_factor=0, total=None, status=3, status_forcelist={500}),
        reraise=True,
    )
    retrying_request = retrying.wraps(httpx.request)

    with pytest.raises(tenacity.RetryError):
        retrying_request('GET', 'http://example.com', timeout=0.1)
    assert retrying.statistics['attempt_number'] == 4
