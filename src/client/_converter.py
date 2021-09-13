__all__: list = []
import datetime
from decimal import Decimal
import re
import sys
import uuid
from typing import List, Union

import cattr
from .util._extendable_enum import ExtendableStrEnum

if sys.version_info[:2] < (3, 7):
    from backports.datetime_fromisoformat import MonkeyPatch
    MonkeyPatch.patch_fromisoformat()


converter = cattr.Converter()

converter.register_structure_hook_func(
    lambda type_: hasattr(type_, 'structure'),
    lambda data, type_: type_.structure(data)  # type: ignore
)
converter.register_unstructure_hook_func(  # type: ignore
    lambda obj: hasattr(obj, 'unstructure'),
    lambda obj: obj.unstructure()  # type: ignore
)


converter.register_structure_hook(uuid.UUID, lambda data, type_: type_(data))  # type: ignore
converter.register_unstructure_hook(uuid.UUID, str)

converter.register_structure_hook(
    Union[str, List[str]],
    lambda data, type_: converter.structure(data, List[str] if isinstance(data, list) else str)  # type: ignore
)

MS_IN_ISO_REGEX = re.compile(r'(?<=.{19})\.\d*')


def str_to_datetime(str_dt: str) -> datetime.datetime:
    # Some dirty fix for not matching miliseconds
    # The problem is that sometimes we get here 5 digits in ms. That leads to raising an exception.
    # drop after TOLOKA-16759
    def fill_miliseconds(miliseconds) -> str:
        return miliseconds.group().ljust(7 if len(miliseconds.group()) > 4 else 4, '0')

    return datetime.datetime.fromisoformat(MS_IN_ISO_REGEX.sub(fill_miliseconds, str_dt))


# Dates are represented as ISO 8601: YYYY-MM-DDThh:mm:ss[.sss]
# and structured to datetime.datetime
converter.register_structure_hook(
    datetime.datetime,
    lambda data, type_: data if isinstance(data, datetime.datetime) else str_to_datetime(data)  # type: ignore
)
converter.register_unstructure_hook(datetime.datetime, lambda data: data.isoformat())  # type: ignore


converter.register_structure_hook(
    Decimal,
    lambda data, type_: Decimal(data)  # type: ignore
)

# We need to redefine structure/unstructure hook for ExtendableStrEnum because hasattr(type_, 'structure') works
# incorrect in that case
converter.register_unstructure_hook(ExtendableStrEnum, converter._unstructure_enum)
converter.register_structure_hook(ExtendableStrEnum, converter._structure_call)


structure = converter.structure
unstructure = converter.unstructure
