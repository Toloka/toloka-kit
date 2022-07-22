__all__ = [
    'AsyncInterfaceWrapper',
    'AsyncMultithreadWrapper',
    'ComplexException',
    'ensure_async',
    'get_task_traceback',
    'Cooldown',
]

import asyncio
import attr
import functools
import pickle
from concurrent import futures
import contextvars
from io import StringIO
import time
from typing import Awaitable, Callable, Dict, Generic, List, Optional, Type, TypeVar

from .stored import PICKLE_DEFAULT_PROTOCOL


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


@attr.s
class _EnsureAsynced:
    __wrapped__: Callable = attr.ib()

    async def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)


def ensure_async(func: Callable) -> Callable[..., Awaitable]:
    """Ensure given callable is async.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.

    Args:
        func: Any callable: synchronous or asynchronous.
    Returns:
        Wrapper that return awaitable object at call.
    """

    if asyncio.iscoroutinefunction(func) or asyncio.iscoroutinefunction(getattr(func, '__call__', None)):
        return func
    return functools.wraps(func)(_EnsureAsynced(func))


T = TypeVar('T')


class AsyncInterfaceWrapper(Generic[T]):
    """Wrap arbitrary object to be able to await any of it's methods even if it's sync.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.
    """

    def __init__(self, wrapped: T):
        self.__wrapped__ = wrapped

    def __getstate__(self) -> bytes:
        return pickle.dumps(self.__wrapped__, protocol=PICKLE_DEFAULT_PROTOCOL)

    def __setstate__(self, state: bytes) -> None:
        self.__wrapped__ = pickle.loads(state)

    def __getattr__(self, name: str):
        attribute = getattr(self.__wrapped__, name)
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
        self.__wrapped__ = wrapped
        self.__loop = loop
        self.__pool_size = pool_size
        self.__executor = futures.ThreadPoolExecutor(max_workers=pool_size)

    @property
    def _loop(self):
        if self.__loop is None:
            self.__loop = asyncio.get_event_loop()
        return self.__loop

    def __getstate__(self) -> bytes:
        return pickle.dumps((self.__wrapped__, self.__pool_size), protocol=PICKLE_DEFAULT_PROTOCOL)

    def __setstate__(self, state: bytes) -> None:
        self.__wrapped__, self.__pool_size = pickle.loads(state)
        self.__executor = futures.ThreadPoolExecutor(max_workers=self.__pool_size)

    def __getattr__(self, name: str):
        attribute = getattr(self.__wrapped__, name)
        if not callable(attribute):
            return attribute

        @functools.wraps(attribute)
        async def _wrapper(*args, **kwargs):

            def func_with_init_vars(*args, **kwargs):
                func, ctx_vars, *args_for_func = args
                for var, value in ctx_vars.items():
                    var.set(value)
                return func(*args_for_func, **kwargs)

            ctx = contextvars.copy_context()
            return await self._loop.run_in_executor(
                self.__executor,
                functools.partial(func_with_init_vars, attribute, ctx, *args, **kwargs)
            )

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


class Cooldown:
    """Сontext manager that implements a delay between calls occurring inside the context

    Args:
        cooldown_time(int): seconds between calls

    Example:
        >>> coldown = toloka.util.Cooldown(5)
        >>> while True:
        >>>     async with coldown:
        >>>         await do_it()  # will be called no more than once every 5 seconds
        ...
    """
    _touch_time: float
    _cooldown_time: int

    def __init__(self, cooldown_time):
        self._touch_time = None
        self._cooldown_time = cooldown_time

    async def __aenter__(self):
        if self._touch_time:
            time_to_sleep = self._cooldown_time + self._touch_time - time.time()
            if time_to_sleep > 0:
                await asyncio.sleep(time_to_sleep)
        self._touch_time = time.time()

    async def __aexit__(self, *exc):
        pass
