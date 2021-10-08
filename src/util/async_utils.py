__all__ = [
    'AsyncInterfaceWrapper',
    'AsyncMultithreadWrapper',
    'ComplexException',
    'ensure_async',
    'get_task_traceback',
]

import asyncio
import attr
import functools
from concurrent import futures
from io import StringIO
from typing import Awaitable, Callable, Dict, Generic, List, Optional, Type, TypeVar


@attr.s
class ComplexException(Exception):
    """Exception to aggregate multiple exceptions occured.
    Unnderlying exceptions are stored in the `exceptions` attribute.

    Attributes:
        exceptions: List of underlying exceptions.
    """
    exceptions: List[Exception] = attr.ib()

    def __attrs_post_init__(self) -> None:
        aggregated_by_type: Dict[Type, ComplexException] = {}
        flat: List[Exception] = []

        self_class = type(self)
        for exc in self.exceptions:
            exc_class = type(exc)
            if exc_class is self_class:
                flat.extend(exc.exceptions)
            elif isinstance(exc, ComplexException):
                if exc_class in aggregated_by_type:
                    aggregated_by_type[exc_class].exceptions.extend(exc.exceptions)
                else:
                    aggregated_by_type[exc_class] = exc
            else:
                flat.append(exc)

        self.exceptions = list(aggregated_by_type.values()) + flat

        raise self


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

    if asyncio.iscoroutinefunction(func) or asyncio.iscoroutinefunction(getattr(func, '__call__', None)):
        return func

    return _async_wrapper


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


def get_task_traceback(task: asyncio.Task) -> Optional[str]:
    """Get traceback for given task as string.
    Return traceback as string if exists. Or None if there was no error.
    """
    if task.exception() is None:
        return None
    with StringIO() as stream:
        task.print_stack(file=stream)
        stream.flush()
        stream.seek(0)
        return stream.read()
