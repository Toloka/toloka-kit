from contextvars import ContextVar, Context
from pandas import DataFrame

DESCRIBED_OBJECTS = {
    ContextVar: ('contextvars', 'ContextVar'),
    Context: ('contextvars', 'Context'),
    DataFrame: ('pandas', 'DataFrame'),
    None: ('builtins', 'None'),
}
