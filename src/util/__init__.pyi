__all__ = [
    'AsyncMultithreadWrapper',
    'get_signature',
]
import inspect
import typing

from toloka.util.async_utils import AsyncMultithreadWrapper

def get_signature(func: typing.Callable) -> inspect.Signature:
    """Correctly processes a signature for a callable. Correctly processes
    classes
    """
    ...
