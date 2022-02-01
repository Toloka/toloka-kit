__all__ = [
    'add_headers',
    'async_add_headers',
    'caller_context_var',
    'top_level_method_var',
    'low_level_method_var',
]
import contextvars


caller_context_var: contextvars.ContextVar

top_level_method_var: contextvars.ContextVar

low_level_method_var: contextvars.ContextVar

def add_headers(client: str):
    """This decorator add 3 headers into resulting http request:
    1) X-Caller-Context: high-level abstraction like client, metrics, streaming
    2) X-Top-Level-Method: first function, that was called and then called other functions which provoked request
    3) X-Low-Level-Method: last function before calling TolokaClient _method (_raw_request for example)

    Args:
        client: name of high-level abstraction for X-Caller-Context
    """
    ...


def async_add_headers(client: str):
    """This decorator add 3 headers into resulting http request called by async function:
    1) X-Caller-Context: high-level abstraction like client, metrics, streaming
    2) X-Top-Level-Method: first function, that was called and then called other functions which provoked request
    3) X-Low-Level-Method: last function before calling TolokaClient _method (_raw_request for example)

    Args:
        client: name of high-level abstraction for X-Caller-Context
    """
    ...
