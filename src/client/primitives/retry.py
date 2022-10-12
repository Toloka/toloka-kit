__all__ = [
    'TolokaRetry', 'SyncRetryingOverURLLibRetry', 'AsyncRetryingOverURLLibRetry'
]

import json
import logging
import socket
from functools import wraps
from inspect import signature
from typing import Callable, List, Optional, Tuple, Type, Union

import httpx
import urllib3
import urllib3.exceptions
from tenacity import AsyncRetrying, BaseRetrying, RetryCallState, Retrying
from tenacity.retry import retry_base
from tenacity.stop import stop_base
from tenacity.wait import wait_base
from urllib3.connectionpool import ConnectionPool
from urllib3.response import HTTPResponse  # type: ignore
from urllib3.util.retry import Retry  # type: ignore

logger = logging.getLogger(__name__)

STATUSES_TO_RETRY = {408, 429, 500, 503, 504}


class TolokaRetry(Retry):
    """Retry toloka quotas. By default only minutes quotas.

    Args:
        retry_quotas (Union[List[str], str, None]): List of quotas that will be retried.
            None or empty list for not retrying quotas.
            You can specify quotas:
            * MIN - Retry minutes quotas.
            * HOUR - Retry hourly quotas. This is means that the program just sleeps for an hour! Be careful.
            * DAY - Retry daily quotas. We strongly not recommended retrying these quotas.
    """
    class Unit:
        MIN = 'MIN'
        HOUR = 'HOUR'
        DAY = 'DAY'

    seconds_to_wait = {
        Unit.MIN: 60,
        Unit.HOUR: 60*60,
        Unit.DAY: 60*60*24,
    }

    _retry_quotas: Union[List[str], str, None] = None

    def __init__(self, *args, retry_quotas: Union[List[str], str, None] = Unit.MIN, **kwargs):
        if isinstance(retry_quotas, str):
            self._retry_quotas = [retry_quotas]
        else:
            self._retry_quotas = retry_quotas

        self._last_response = kwargs.pop('last_response', None)
        super(TolokaRetry, self).__init__(*args, **kwargs)

    def new(self, **kwargs):
        kwargs['last_response'] = self._last_response
        return super(TolokaRetry, self).new(retry_quotas=self._retry_quotas, **kwargs)

    def get_retry_after(self, response: HTTPResponse) -> Optional[float]:
        seconds = super(TolokaRetry, self).get_retry_after(response)
        if seconds is not None:
            return seconds

        if response.status != 429 or self._retry_quotas is None or self._last_response is None:
            return None
        payload = self._last_response.get('payload', None)
        if payload is None or 'interval' not in payload:
            return None

        interval = payload['interval']
        if interval not in self._retry_quotas:
            return None

        if interval == TolokaRetry.Unit.HOUR:
            logger.warning('The limit on hourly quotas worked. The program "falls asleep" for an hour.')
        if interval == TolokaRetry.Unit.DAY:
            logger.warning('The daily quota limit worked. The program "falls asleep" for the day.')
        return TolokaRetry.seconds_to_wait.get(interval, None)

    def increment(self, *args, **kwargs) -> Retry:
        self._last_response = None
        response = kwargs.get('response', None)
        try:
            if response is not None:
                data = response.data
                if data:
                    self._last_response = json.loads(response.data.decode("utf-8"))
        except json.JSONDecodeError:
            pass
        return super(TolokaRetry, self).increment(*args, **kwargs)


def httpx_exception_to_urllib_exception(exception: BaseException) -> BaseException:
    """Maps the httpx exception to the corresponding urllib3 exception."""

    if isinstance(exception, httpx.HTTPError):
        mapped_exception = urllib3.exceptions.HTTPError()
    elif isinstance(exception, httpx.RequestError):
        mapped_exception = urllib3.exceptions.RequestError(
            pool=ConnectionPool(str(exception.request.url)), url=str(exception.request.url), message=str(exception)
        )
    elif isinstance(exception, httpx.TransportError):
        mapped_exception = urllib3.exceptions.HTTPError(),
    elif isinstance(exception, httpx.TimeoutException):
        mapped_exception = urllib3.exceptions.TimeoutError(),
    elif isinstance(exception, httpx.ConnectTimeout):
        mapped_exception = urllib3.exceptions.ConnectTimeoutError(),
    elif isinstance(exception, httpx.ReadTimeout):
        mapped_exception = urllib3.exceptions.ReadTimeoutError(
            pool=ConnectionPool(str(exception.request.url)), url=str(exception.request.url), message=str(exception)
        )
    elif isinstance(exception, httpx.WriteTimeout):
        return socket.timeout()
    elif isinstance(exception, httpx.PoolTimeout):
        mapped_exception = urllib3.exceptions.NewConnectionError(
            pool=ConnectionPool(str(exception.request.url)), message=str(exception)
        )
    elif isinstance(exception, httpx.NetworkError):
        mapped_exception = urllib3.exceptions.HTTPError()
    elif isinstance(exception, httpx.ConnectError):
        mapped_exception = urllib3.exceptions.ConnectionError()
    elif isinstance(exception, httpx.ReadError):
        mapped_exception = socket.error()
    elif isinstance(exception, httpx.WriteError):
        mapped_exception = socket.error()
    elif isinstance(exception, httpx.CloseError):
        mapped_exception = urllib3.exceptions.ConnectionError()
    elif isinstance(exception, httpx.ProtocolError):
        mapped_exception = urllib3.exceptions.ProtocolError()
    elif isinstance(exception, httpx.LocalProtocolError):
        mapped_exception = urllib3.exceptions.ProtocolError()
    elif isinstance(exception, httpx.RemoteProtocolError):
        mapped_exception = urllib3.exceptions.ProtocolError()
    elif isinstance(exception, httpx.ProxyError):
        mapped_exception = urllib3.exceptions.ProxyError(error=exception, message=str(exception))
    elif isinstance(exception, httpx.UnsupportedProtocol):
        mapped_exception = urllib3.exceptions.URLSchemeUnknown(scheme=exception.request.url.scheme)
    elif isinstance(exception, httpx.DecodingError):
        mapped_exception = urllib3.exceptions.DecodeError()
    elif isinstance(exception, httpx.TooManyRedirects):
        mapped_exception = urllib3.exceptions.ResponseError()
    elif isinstance(exception, httpx.HTTPStatusError):
        mapped_exception = urllib3.exceptions.ResponseError()
    elif isinstance(exception, httpx.InvalidURL):
        mapped_exception = urllib3.exceptions.LocationValueError()
    elif isinstance(exception, httpx.CookieConflict):
        mapped_exception = urllib3.exceptions.ResponseError()
    elif isinstance(exception, httpx.StreamError):
        mapped_exception = socket.error()
    elif isinstance(exception, httpx.StreamConsumed):
        mapped_exception = socket.error()
    elif isinstance(exception, httpx.StreamClosed):
        mapped_exception = socket.error()
    else:
        mapped_exception = urllib3.exceptions.HTTPError()
    mapped_exception.__cause__ = exception
    return mapped_exception


class RetryingOverURLLibRetry(BaseRetrying):
    """Adapter class that allows usage of the urllib3 Retry class with the tenacity retrying mechanism.

    Wrapped function should make a single request using HTTPX library and either return httpx.Response or raise an
    exception.
    """

    def __init__(self, base_url: str, retry: Retry, exception_to_retry: Tuple[Type[Exception], ...], **kwargs):
        self.base_url = base_url
        self.urllib_retry = retry
        self.exception_to_retry = exception_to_retry

        super().__init__(
            stop=self._get_stop_callback(),
            wait=self._get_wait_callback(),
            after=self._get_after_callback(),
            retry=self._get_retry_callback(),
            **kwargs,
        )

    def __getstate__(self):
        return {
            'base_url': self.base_url, 'urllib_retry': self.urllib_retry, 'exception_to_retry': self.exception_to_retry
        }

    def __setstate__(self, state):
        self.__init__(
            base_url=state['base_url'], retry=state['urllib_retry'], exception_to_retry=state['exception_to_retry']
        )

    def _patch_with_urllib_retry(self, func: Callable):
        """Ensures that retry_state contains current urllib3 Retry instance before function call."""

        @wraps(func)
        def wrapped(*args, **kwargs):
            bound_args = signature(func).bind(*args, **kwargs)
            retry_state = bound_args.arguments['retry_state']
            if getattr(retry_state, 'urllib_retry', None) is None:
                retry_state.urllib_retry = self.urllib_retry
            return func(*args, **kwargs)
        return wrapped

    @staticmethod
    def _get_urllib_response(retry_state: RetryCallState):
        """Constructs urllib3 response from httpx response."""

        if retry_state.outcome.failed:
            return None

        _httpx_to_urllib_http_version = {'HTTP/2': 20, 'HTTP/1.1': 11}
        httpx_response: httpx.Response = retry_state.outcome.result()
        return urllib3.HTTPResponse(
            body=httpx_response.content,
            headers=httpx_response.headers,
            status=httpx_response.status_code,
            version=_httpx_to_urllib_http_version[httpx_response.http_version],
            reason=httpx_response.reason_phrase,
            preload_content=True,
            decode_content=False,
            request_method=httpx_response.request.method,
            request_url=httpx_response.request.url,
        )

    def _get_stop_callback(self):

        class IsExhausted(stop_base):
            """Callback wrapped in callable class to match BaseRetrying signature."""

            @self._patch_with_urllib_retry
            def __call__(self, retry_state):
                return retry_state.urllib_retry.is_exhausted()

        return IsExhausted()

    def _get_wait_callback(self):
        outer_self = self

        class GetBackoffTime(wait_base):
            """Callback wrapped in callable class to match BaseRetrying signature."""

            @self._patch_with_urllib_retry
            def __call__(self, retry_state):
                response = outer_self._get_urllib_response(retry_state)
                if response and retry_state.urllib_retry.respect_retry_after_header:
                    retry_after = retry_state.urllib_retry.get_retry_after(response)
                    if retry_after:
                        return retry_state
                return retry_state.urllib_retry.get_backoff_time()

        return GetBackoffTime()

    def _get_retry_callback(self):

        class IsRetry(retry_base):
            """Callback wrapped in callable class to match BaseRetrying signature."""

            @self._patch_with_urllib_retry
            def __call__(self, retry_state):
                if retry_state.outcome.failed:
                    exception = retry_state.outcome.exception()
                    return isinstance(exception, retry_state.retry_object.exception_to_retry)

                httpx_response: httpx.Response = retry_state.outcome.result()
                has_retry_after = bool(httpx_response.headers.get("Retry-After", False))

                return retry_state.urllib_retry.is_retry(
                    method=httpx_response.request.method, status_code=httpx_response.status_code,
                    has_retry_after=has_retry_after
                )

        return IsRetry()

    def _get_after_callback(self):

        @self._patch_with_urllib_retry
        def increment(retry_state: RetryCallState):
            retry: Retry = retry_state.urllib_retry
            bound_args = signature(retry_state.fn).bind(*retry_state.args, **retry_state.kwargs)

            response = self._get_urllib_response(retry_state)
            exception = retry_state.outcome.exception() if retry_state.outcome.failed else None

            try:
                retry_state.urllib_retry = retry.increment(
                    method=bound_args.arguments['method'],
                    url=f'{self.base_url}{bound_args.arguments["path"]}',
                    response=response,
                    error=httpx_exception_to_urllib_exception(exception) if exception else None,
                )
            except urllib3.exceptions.MaxRetryError:
                # retry.increment raises MaxRetryError when exhausted. We want to delegate checking if the process
                # should be stopped to the stop callback.
                retry_state.urllib_retry = Retry(total=-1)

        return increment


class SyncRetryingOverURLLibRetry(RetryingOverURLLibRetry, Retrying):
    pass


class AsyncRetryingOverURLLibRetry(RetryingOverURLLibRetry, AsyncRetrying):
    pass
