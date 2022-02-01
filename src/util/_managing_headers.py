__all__ = [
    'add_headers',
    'async_add_headers',
    'caller_context_var',
    'top_level_method_var',
    'low_level_method_var',
]
from contextvars import ContextVar, copy_context
import functools
from contextlib import ExitStack

caller_context_var: ContextVar = ContextVar('caller_context')
top_level_method_var: ContextVar = ContextVar('top_level_method')
low_level_method_var: ContextVar = ContextVar('low_level_method')


class SetVariable:

    def __init__(self, var, value):
        self.var = var
        self.value = value
        self.token = None

    def __enter__(self):
        self.token = self.var.set(self.value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.token:
            self.var.reset(self.token)


def add_headers(client: str):
    """
    This decorator add 3 headers into resulting http request:
    1) X-Caller-Context: high-level abstraction like client, metrics, streaming
    2) X-Top-Level-Method: first function, that was called and then called other functions which provoked request
    3) X-Low-Level-Method: last function before calling TolokaClient _method (_raw_request for example)

    Args:
        client: name of high-level abstraction for X-Caller-Context
    """

    def wrapper(func):

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            ctx = copy_context()
            with ExitStack() as stack:
                stack.enter_context(SetVariable(low_level_method_var, func.__name__))
                if caller_context_var not in ctx:
                    stack.enter_context(SetVariable(caller_context_var, client))
                if top_level_method_var not in ctx:
                    stack.enter_context(SetVariable(top_level_method_var, func.__name__))

                return func(*args, **kwargs)

        return wrapped

    return wrapper


def async_add_headers(client: str):
    """
    This decorator add 3 headers into resulting http request called by async function:
    1) X-Caller-Context: high-level abstraction like client, metrics, streaming
    2) X-Top-Level-Method: first function, that was called and then called other functions which provoked request
    3) X-Low-Level-Method: last function before calling TolokaClient _method (_raw_request for example)

    Args:
        client: name of high-level abstraction for X-Caller-Context
    """

    def wrapper(func):

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            ctx = copy_context()
            with ExitStack() as stack:
                stack.enter_context(SetVariable(low_level_method_var, func.__name__))
                if caller_context_var not in ctx:
                    stack.enter_context(SetVariable(caller_context_var, client))
                if top_level_method_var not in ctx:
                    stack.enter_context(SetVariable(top_level_method_var, func.__name__))

                return await func(*args, **kwargs)

        return wrapped

    return wrapper
