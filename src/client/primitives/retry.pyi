__all__ = [
    'TolokaRetry',
]
from requests.packages.urllib3.response import HTTPResponse
from requests.packages.urllib3.util.retry import Retry
from typing import (
    List,
    Optional,
    Union
)

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
        ...

    def __init__(
        self,
        *args,
        retry_quotas: Union[List[str], str, None] = 'MIN',
        **kwargs
    ): ...

    def get_retry_after(self, response: HTTPResponse) -> Optional[float]: ...

    def increment(
        self,
        *args,
        **kwargs
    ) -> 'Retry': ...

    def new(self, **kwargs): ...

    _retry_quotas: Union[List[str], str, None]
