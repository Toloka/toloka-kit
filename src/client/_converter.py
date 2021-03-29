__all__: list = []
import datetime
from decimal import Decimal
import sys
import uuid
from typing import List, Union

import cattr

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


# Dates are are represented as ISO 8601: YYYY-MM-DDThh:mm:ss[.sss]
# and structured to datetime.datetime
converter.register_structure_hook(
    datetime.datetime,
    lambda data, type_: data if isinstance(data, datetime.datetime) else type_.fromisoformat(data)  # type: ignore
)
converter.register_unstructure_hook(datetime.datetime, lambda data: data.isoformat())  # type: ignore


converter.register_structure_hook(
    Decimal,
    lambda data, type_: Decimal(data)  # type: ignore
)


structure = converter.structure
unstructure = converter.unstructure
