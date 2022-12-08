__all__ = [
    'TolokaRetry',
    'SyncRetryingOverURLLibRetry',
    'AsyncRetryingOverURLLibRetry',
]
import abc
import tenacity
import typing
import urllib3.response
import urllib3.util.retry


class TolokaRetry(urllib3.util.retry.Retry):
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

    def get_retry_after(self, response: urllib3.response.HTTPResponse) -> typing.Optional[float]: ...

    def increment(
        self,
        *args,
        **kwargs
    ) -> urllib3.util.retry.Retry: ...

    _retry_quotas: typing.Union[typing.List[str], str, None]


class RetryingOverURLLibRetry(tenacity.BaseRetrying, metaclass=abc.ABCMeta):
    """Adapter class that allows usage of the urllib3 Retry class with the tenacity retrying mechanism.

    Wrapped function should make a single request using HTTPX library and either return httpx.Response or raise an
    exception.
    """

    def __init__(
        self,
        base_url: str,
        retry: urllib3.util.retry.Retry,
        exception_to_retry: typing.Tuple[typing.Type[Exception], ...],
        **kwargs
    ): ...

    def __getstate__(self): ...

    def __setstate__(self, state): ...


class SyncRetryingOverURLLibRetry(RetryingOverURLLibRetry, tenacity.Retrying):
    ...


class AsyncRetryingOverURLLibRetry(RetryingOverURLLibRetry, tenacity.AsyncRetrying):
    ...
