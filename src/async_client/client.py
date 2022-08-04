__all__ = [
    'AsyncTolokaClient',
]

import asyncio
import datetime
import inspect
import linecache
import logging
import os.path
import re
import sys
import uuid
from decimal import Decimal
from typing import Union, Tuple, Optional, List, Callable

import httpx
from functools import wraps
from textwrap import dedent

from urllib3 import Retry

from ..util._managing_headers import async_add_headers, form_additional_headers
from ..client import TolokaClient, operations
from ..client.primitives.retry import TolokaRetry

logger = logging.getLogger(__name__)


def generate_async_methods_from(cls):
    def _generate_async_version_source(method):
        yield_from_regex = re.compile(r'yield from ([\S]+)')
        source = re.sub(
            yield_from_regex,
            r'async for _val in \1: yield _val',
            inspect.getsource(method),
        )

        method_call_regex = re.compile(r'(?<!in )(self\.\w+\()')
        source = re.sub(method_call_regex, r'await \1', source)

        source = source.replace(
            f'def {method.__name__}', f'async def {method.__name__}'
        )
        source = source.replace("add_headers('client')", "async_add_headers('async_client')")
        return dedent(source)

    def _compile_function(member_name, source):
        file_name = f'async_client_{member_name}'

        bytecode = compile(source, file_name, 'exec')
        proxy_globals = dict(**sys.modules[cls.__module__].__dict__)
        proxy_globals['async_add_headers'] = async_add_headers
        proxy_locals = dict(**cls.__dict__)
        eval(bytecode, proxy_globals, proxy_locals)
        function = proxy_locals[member_name]
        function.__module__ = __name__

        linecache.cache[file_name] = (
            len(source),
            None,
            source.splitlines(True),
            file_name
        )

        return function

    def wrapper(target_cls):
        for member_name, member in cls.__dict__.items():
            if (
                inspect.isfunction(member)
                and not hasattr(target_cls, member_name)
                and not isinstance(member_name, property)
            ):
                source = _generate_async_version_source(member)

                function = _compile_function(member_name, source)
                setattr(target_cls, member_name, function)
        return target_cls

    return wrapper


@generate_async_methods_from(TolokaClient)
class AsyncTolokaClient:
    """Class that implements interaction with [Toloka API](https://toloka.ai/docs/api/concepts/about.html), in an asynchronous way.

    All methods are wrapped as async. So all methods calls must be awaited.
    All arguments, same as in TolokaClient.
    """

    retry_prototype: Retry

    def __init__(
        self,
        token: str,
        environment: Union[TolokaClient.Environment, str, None] = None,
        retries: Union[int, Retry] = 3,
        timeout: Union[float, Tuple[float, float]] = 10.0,
        url: Optional[str] = None,
        retry_quotas: Union[List[str], str, None] = TolokaRetry.Unit.MIN,
        retryer_factory: Optional[Callable[[], Retry]] = None,
        act_under_account_id: Optional[str] = None,
    ):
        self._sync_client = TolokaClient(
            token=token, environment=environment, timeout=timeout, url=url, act_under_account_id=act_under_account_id,
        )

        if isinstance(retries, Retry):
            self.retry_prototype = retries
        elif retryer_factory:
            self.retry_prototype = retryer_factory()
        else:
            self.retry_prototype = self._sync_client._default_retryer_factory(retries, retry_quotas)

    @classmethod
    def from_sync_client(cls, client: TolokaClient) -> 'AsyncTolokaClient':
        async_client = cls.__new__(cls)
        async_client._sync_client = client
        async_client.retry_prototype = client.retryer_factory()
        return async_client

    @property
    def sync_client(self) -> TolokaClient:
        return self._sync_client

    def __getattr__(self, name):
        return getattr(self._sync_client, name)

    # @functools.lru_cache(maxsize=128)
    # def _session_for_thread(self, thread_id: int) -> requests.Session:
    #     adapter = PreloadingHTTPAdapter(max_retries=self.retryer_factory())
    #     session = requests.Session()
    #     session.mount(self.url, adapter)
    #     session.headers.update(
    #         {
    #             'Authorization': f'OAuth {self.token}',
    #             'User-Agent': f'python-toloka-client-{__version__}',
    #         }
    #     )
    #     if self.act_under_account_id:
    #         session.headers['X-Act-Under-Account-ID'] = self.act_under_account_id
    #     return session
    #
    @property
    def _session(self):
        #self.retry_prototype
        #transport = httpx.AsyncHTTPTransport(retries=)
        client = httpx.AsyncClient(headers=self._headers, base_url=self.url)
        return client

    async def _raw_request(self, method, path, **kwargs):

        # Fixing capitalisation in boolean parameters
        if kwargs.get('params'):
            params = kwargs['params']
            for key, value in params.items():
                if isinstance(value, bool):
                    params[key] = 'true' if value else 'false'
        if self.default_timeout is not None and 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        # Add additional headers from contextvars
        additional_headers = form_additional_headers()
        headers = kwargs.get('headers', {})
        headers = {**headers, **additional_headers}
        kwargs['headers'] = headers

        response = await self._session.request(method, f'{self.url}/api{path}', **kwargs)
        #raise_on_api_error(response)
        return response

    async def _request(self, method, path, **kwargs):
        return (await self._raw_request(method, path, **kwargs)).json(parse_float=Decimal)

    # async def wait_operation(
    #     self,
    #     op: operations.Operation,
    #     timeout: datetime.timedelta = datetime.timedelta(minutes=10),
    #     logger=logger,
    # ) -> operations.Operation:
    #     """Asynchronous version of wait_operation"""
    #     default_time_to_wait = datetime.timedelta(seconds=1)
    #     default_initial_delay = datetime.timedelta(milliseconds=500)
    #
    #     if op.is_completed():
    #         return op
    #
    #     utcnow = datetime.datetime.now(datetime.timezone.utc)
    #     wait_until_time = utcnow + timeout
    #
    #     if not op.started or utcnow - op.started < default_initial_delay:
    #         await asyncio.sleep(default_initial_delay.total_seconds())
    #
    #     while True:
    #         op = await self.get_operation(op.id)
    #         if op.is_completed():
    #             return op
    #         await asyncio.sleep(default_time_to_wait.total_seconds())
    #         if datetime.datetime.now(datetime.timezone.utc) > wait_until_time:
    #             raise TimeoutError
