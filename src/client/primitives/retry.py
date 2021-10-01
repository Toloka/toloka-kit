__all__ = [
    'TolokaRetry', 'PreloadingHTTPAdapter'
]

import json
import logging
from functools import wraps
from requests.adapters import HTTPAdapter
from typing import Optional, List, Union
from urllib3.response import HTTPResponse  # type: ignore
from urllib3.util.retry import Retry  # type: ignore

logger = logging.getLogger(__name__)


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


class PreloadingHTTPAdapter(HTTPAdapter):
    """HTTPAdapter subclass that forces preload_content=True during requests

    As for current version (2.26.0) requests supports body preloading with stream=False, but this behaviour is
    implemented by calling response.content in the end of request process. Such implementation does not support
    retries in case of headers being correctly received by client but body being loaded incorrectly (i.e. when server
    uses chunked transfer encoding and fails during body transmission). Retries are handled on urllib3 level and
    retrying failed body read can be achieved by passing preload_content=False to urllib3.response.HTTPResponse. To do
    this using HTTPAdapter we need to use HTTP(S)ConnectionPool.urlopen with preload_content=True during send method and
    override build_response method to populate requests Response wrapper with content.
    """

    @staticmethod
    def _override_preload_content(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['preload_content'] = True
            kwargs['decode_content'] = True
            resp = func(*args, **kwargs)
            return resp

        return wrapper

    def build_response(self, req, resp):
        response = super().build_response(req, resp)
        response._content = resp.data
        return response

    def get_connection(self, *args, **kwargs):
        connection = super().get_connection(*args, **kwargs)
        connection.urlopen = self._override_preload_content(connection.urlopen)
        return connection
