__all__ = [
    'add_headers',
    'async_add_headers',
    'form_additional_headers',
]
import contextvars
import typing


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


def form_additional_headers(ctx: contextvars.Context = None) -> typing.Dict[str, str]: ...
