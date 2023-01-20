__all__ = [
    'AsyncTolokaClient',
]

import asyncio
import datetime
import functools
import logging
import threading
from decimal import Decimal
from typing import Optional

import attr
import httpx

from ..client import TolokaClient
from ..client.exceptions import (
    raise_on_api_error,
)
from ..client.operations import Operation
from ..client.primitives.retry import AsyncRetryingOverURLLibRetry
from ..util._managing_headers import add_headers
from ..util.async_utils import generate_async_methods_from

logger = logging.getLogger(__name__)


@generate_async_methods_from(TolokaClient)
class AsyncTolokaClient:
    """Class that implements interaction with [Toloka API](https://toloka.ai/en/docs/api/), in an asynchronous way.

    All methods are wrapped as async. So all methods calls must be awaited.
    All arguments, same as in TolokaClient.
    """

    @functools.wraps(TolokaClient.__init__)
    def __init__(
        self,
        *args, **kwargs
    ):
        self._sync_client = TolokaClient(*args, **kwargs)
        self.retrying = AsyncRetryingOverURLLibRetry(
            base_url=str(self._session.base_url), retry=self._sync_client.retryer_factory(), reraise=True,
            exception_to_retry=self.EXCEPTIONS_TO_RETRY,
        )

    def __getattr__(self, name):
        """Access non function fields.

        All function fields should be already overridden with `generate_async_methods_from`."""
        return getattr(self._sync_client, name)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    @classmethod
    def from_sync_client(cls, client: TolokaClient) -> 'AsyncTolokaClient':
        async_client = cls.__new__(cls)
        async_client.__init__(
            token=client.token, url=client.url, retries=client.retryer_factory(), timeout=client.default_timeout,
            act_under_account_id=client.act_under_account_id, retry_quotas=None,
        )
        async_client._sync_client = client
        return async_client

    @property
    def sync_client(self) -> TolokaClient:
        return self._sync_client

    @functools.lru_cache(maxsize=128)
    def _session_for_thread(self, thread_id: int) -> httpx.AsyncClient:
        client = httpx.AsyncClient(headers=self._headers, base_url=self.url)
        return client

    @property
    def _session(self):
        return self._session_for_thread(threading.current_thread().ident)

    async def _do_request_with_retries(self, method, path, **kwargs):
        @self.retrying.wraps
        async def wrapped(method, path, **kwargs):
            response = await self._session.request(method, path, **kwargs)
            await response.aread()
            raise_on_api_error(response)
            return response

        return await wrapped(method, path, **kwargs)

    async def _request(self, method, path, **kwargs):
        return (await self._raw_request(method, path, **kwargs)).json(parse_float=Decimal)

    async def _find_all(self, find_function, request, sort_field: str = 'id',
                        items_field: str = 'items', batch_size: Optional[int] = None):
        result = await find_function(request, sort=[sort_field], limit=batch_size)
        items = getattr(result, items_field)
        while result.has_more:
            request = attr.evolve(request, **{f'{sort_field}_gt': getattr(items[-1], sort_field)})
            for item in items:
                yield item
            result = await find_function(request, sort=[sort_field])
            items = getattr(result, items_field)

        for item in items:
            yield item

    async def _collect_from_pools(self, get_method, pools):
        items = {}
        for pool_id, numerated_ids in pools.items():
            obj_it = get_method(
                pool_id=pool_id,
                id_gte=min(numerated_ids.keys()),
                id_lte=max(numerated_ids.keys()),
            )
            async for obj in obj_it:
                if obj.id in numerated_ids:
                    items[numerated_ids[obj.id]] = obj
        return items

    @add_headers('async_client')
    async def wait_operation(
        self,
        op: Operation,
        timeout: datetime.timedelta = datetime.timedelta(minutes=10),
        logger=logger,
    ) -> Operation:
        """Asynchronous version of wait_operation"""
        default_time_to_wait = datetime.timedelta(seconds=1)
        default_initial_delay = datetime.timedelta(milliseconds=500)

        if op.is_completed():
            return op

        utcnow = datetime.datetime.now(datetime.timezone.utc)
        wait_until_time = utcnow + timeout

        if not op.started or utcnow - op.started < default_initial_delay:
            await asyncio.sleep(default_initial_delay.total_seconds())

        while True:
            op = await self.get_operation(op.id)
            if op.is_completed():
                return op
            await asyncio.sleep(default_time_to_wait.total_seconds())
            if datetime.datetime.now(datetime.timezone.utc) > wait_until_time:
                raise TimeoutError
