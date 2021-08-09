__all__ = [
    'AsyncInterfaceWrapper',
    'AsyncMultithreadWrapper',
    'ensure_async',
]

import asyncio
import functools
from concurrent import futures
from typing import Awaitable, Callable, Generic, Optional, TypeVar


def ensure_async(func: Callable) -> Callable[..., Awaitable]:
    """Ensure given callable is async.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.

    Args:
        func: Any callable: synchronous or asynchronous.
    Returns:
        Wrapper that return awaitable object at call.
    """

    @functools.wraps(func)
    async def _async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return func if asyncio.iscoroutinefunction(func) else _async_wrapper


T = TypeVar('T')


class AsyncInterfaceWrapper(Generic[T]):
    """Wrap arbitrary object to be able to await any of it's methods even if it's sync.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.
    """

    def __init__(self, wrapped: T):
        self.__wrapped = wrapped

    def __getattr__(self, name: str):
        attribute = getattr(self.__wrapped, name)
        return ensure_async(attribute) if callable(attribute) else attribute


class AsyncMultithreadWrapper(Generic[T]):
    """Wrap arbitrary object to run each of it's methods in a separate thread.

    Examples:
        Simple usage example.

        >>> class SyncClassExample:
        >>>     def sync_method(self, sec):
        >>>         time.sleep(sec)  # Definitely not async.
        >>>         return sec
        >>>
        >>> obj = AsyncMultithreadWrapper(SyncClassExample())
        >>> await asyncio.gather(*[obj.sync_method(1) for _ in range(10)])
        ...
    """

    def __init__(self, wrapped: T, pool_size: int = 10, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.__wrapped = wrapped
        self.__executor = futures.ThreadPoolExecutor(max_workers=pool_size)
        self.__loop = loop

    @property
    def _loop(self):
        if self.__loop is None:
            self.__loop = asyncio.get_event_loop()
        return self.__loop

    def __getattr__(self, name: str):
        attribute = getattr(self.__wrapped, name)
        if not callable(attribute):
            return attribute

        @functools.wraps(attribute)
        async def _wrapper(*args, **kwargs):
            return await self._loop.run_in_executor(self.__executor, functools.partial(attribute, *args, **kwargs))

        return _wrapper
