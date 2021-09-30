__all__ = [
    'TolokaRetry',
    'PreloadingHTTPAdapter',
]
import requests.adapters
import requests.packages.urllib3.response
import requests.packages.urllib3.util.retry
import typing


class TolokaRetry(requests.packages.urllib3.util.retry.Retry):
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
        ...

    def __init__(
        self,
        *args,
        retry_quotas: typing.Union[typing.List[str], str, None] = 'MIN',
        **kwargs
    ): ...

    def new(self, **kwargs): ...

    def get_retry_after(self, response: requests.packages.urllib3.response.HTTPResponse) -> typing.Optional[float]: ...

    def increment(
        self,
        *args,
        **kwargs
    ) -> requests.packages.urllib3.util.retry.Retry: ...

    _retry_quotas: typing.Union[typing.List[str], str, None]


class PreloadingHTTPAdapter(requests.adapters.HTTPAdapter):
    """HTTPAdapter subclass that forces preload_content=True during requests

    As for current version (2.26.0) requests supports body preloading with stream=False, but this behaviour is
    implemented by calling response.content in the end of request process. Such implementation does not support
    retries in case of headers being correctly received by client but body being loaded incorrectly (i.e. when server
    uses chunked transfer encoding and fails during body transmission). Retries are handled on urllib3 level and
    retrying failed body read can be achieved by passing preload_content=False to urllib3.response.HTTPResponse. To do
    this using HTTPAdapter we need to use HTTP(S)ConnectionPool.urlopen with preload_content=True during send method and
    override build_response method to populate requests Response wrapper with content.
    """

    def build_response(
        self,
        req,
        resp
    ): ...

    def get_connection(
        self,
        *args,
        **kwargs
    ): ...
