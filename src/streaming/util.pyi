__all__ = [
    'AsyncInterfaceWrapper',
    'AsyncMultithreadWrapper',
    'ComplexException',
    'ensure_async',
    'get_task_traceback',
]
from asyncio import Task
from asyncio.events import AbstractEventLoop
from typing import (
    Awaitable,
    Callable,
    Generic,
    List,
    Optional,
    TypeVar
)


class AsyncInterfaceWrapper(Generic):
    """Wrap arbitrary object to be able to await any of it's methods even if it's sync.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.
    """

    def __init__(self, wrapped: TypeVar('T', bound=None)): ...


class AsyncMultithreadWrapper(Generic):
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

    def __init__(
        self,
        wrapped: TypeVar('T', bound=None),
        pool_size: int = 10,
        loop: Optional[AbstractEventLoop] = None
    ): ...


class ComplexException(Exception):
    """Exception to aggregate multiple exceptions occured.
    Unnderlying exceptions are stored in the `exceptions` attribute.

    Attributes:
        exceptions: List of underlying exceptions.
    """
    exceptions: List[Exception]

    def __init__(self, exceptions: List[Exception]) -> None: ...


def ensure_async(func: Callable) -> Callable[..., Awaitable]:
    """Ensure given callable is async.

    Note, that it doesn't provide concurrency by itself!
    It just allow to treat sync and async callables in the same way.

    Args:
        func: Any callable: synchronous or asynchronous.
    Returns:
        Wrapper that return awaitable object at call.
    """
    ...


def get_task_traceback(task: Task) -> Optional[str]:
    """Get traceback for given task as string.
    Return traceback as string if exists. Or None if there was no error.
    """
    ...
