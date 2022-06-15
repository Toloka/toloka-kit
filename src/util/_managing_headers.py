__all__ = [
    'add_headers',
    'async_add_headers',
    'form_additional_headers',
]

import contextvars
from contextvars import ContextVar, copy_context
import functools
from contextlib import ExitStack, contextmanager
from typing import Dict

caller_context_var: ContextVar = ContextVar('caller_context')
top_level_method_var: ContextVar = ContextVar('top_level_method')
low_level_method_var: ContextVar = ContextVar('low_level_method')


@contextmanager
def set_variable(var, value):
    token = var.set(value)
    try:
        yield copy_context()
    finally:
        if token:
            var.reset(token)


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
                stack.enter_context(set_variable(low_level_method_var, func.__name__))
                if caller_context_var not in ctx:
                    stack.enter_context(set_variable(caller_context_var, client))
                if top_level_method_var not in ctx:
                    stack.enter_context(set_variable(top_level_method_var, func.__name__))

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
                stack.enter_context(set_variable(low_level_method_var, func.__name__))
                if caller_context_var not in ctx:
                    stack.enter_context(set_variable(caller_context_var, client))
                if top_level_method_var not in ctx:
                    stack.enter_context(set_variable(top_level_method_var, func.__name__))

                return await func(*args, **kwargs)

        return wrapped

    return wrapper


def form_additional_headers(ctx: contextvars.Context = None) -> Dict[str, str]:
    if ctx is None:
        ctx = copy_context()
    return {
        'X-Caller-Context': ctx.get(caller_context_var),
        'X-Top-Level-Method': ctx.get(top_level_method_var),
        'X-Low-Level-Method': ctx.get(low_level_method_var),
    }
