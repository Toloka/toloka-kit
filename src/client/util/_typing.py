__all__: list = []
import sys
from typing import Union

if sys.version_info[:2] < (3, 8):

    def get_args(obj):
        return obj.__args__

    def get_origin(obj):
        return getattr(obj, '__origin__', None)

else:
    from typing import get_origin, get_args


def is_optional_of(obj):
    if get_origin(obj) is Union:
        args = get_args(obj)
        if len(args) == 2 and args[1] is type(None):  # noqa
            return args[0]

    return None
