__all__ = [
    'AsyncTolokaClient',
]
import datetime
import toloka.client
import toloka.client.operations


class AsyncTolokaClient:
    """Class that implements interaction with [Toloka API](https://toloka.ai/docs/api/concepts/about.html), in an asynchronous way.

    All methods are wrapped as async. So all methods calls must be awaited.
    All arguments, same as in TolokaClient.
    """

    def __init__(
        self,
        *args,
        **kwargs
    ): ...

    @classmethod
    def from_sync_client(cls, client: toloka.client.TolokaClient) -> 'AsyncTolokaClient': ...

    def wait_operation(
        self,
        op: toloka.client.operations.Operation,
        timeout: datetime.timedelta = ...,
        logger=...
    ) -> toloka.client.operations.Operation:
        """Asynchronous version of wait_operation
        """
        ...
