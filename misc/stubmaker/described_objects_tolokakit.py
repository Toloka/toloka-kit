from contextvars import ContextVar, Context
from pandas import DataFrame
from tenacity import AsyncRetrying

DESCRIBED_OBJECTS = {
    ContextVar: ('contextvars', 'ContextVar'),
    Context: ('contextvars', 'Context'),
    DataFrame: ('pandas', 'DataFrame'),
    AsyncRetrying: ('tenacity', 'AsyncRetrying'),
    None: ('builtins', 'None'),
}
