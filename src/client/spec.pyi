from enum import Enum
from typing import List, Optional


class FieldType(Enum):

    ...

class FieldSpec(object):

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: FieldType,
        required: bool = ...,
        hidden: bool = ...
    ) -> None: ...

    type: FieldType
    required: bool
    hidden: bool

class BooleanSpec(FieldSpec):

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: FieldType,
        required: bool = ...,
        hidden: bool = ...,
        allowed_values: Optional[List[bool]] = ...
    ) -> None: ...

    allowed_values: Optional[List[bool]]

class StringSpec(FieldSpec):

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: FieldType,
        required: bool = ...,
        hidden: bool = ...,
        min_length: Optional[int] = ...,
        max_length: Optional[int] = ...,
        allowed_values: Optional[List[str]] = ...
    ) -> None: ...

    min_length: Optional[int]
    max_length: Optional[int]
    allowed_values: Optional[List[str]]

class IntegerSpec(FieldSpec):

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: FieldType,
        required: bool = ...,
        hidden: bool = ...,
        min_value: Optional[int] = ...,
        max_value: Optional[int] = ...,
        allowed_values: Optional[List[int]] = ...
    ) -> None: ...

    min_value: Optional[int]
    max_value: Optional[int]
    allowed_values: Optional[List[int]]

class FloatSpec(FieldSpec):

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: FieldType,
        required: bool = ...,
        hidden: bool = ...,
        min_value: Optional[float] = ...,
        max_value: Optional[float] = ...
    ) -> None: ...

    min_value: Optional[float]
    max_value: Optional[float]

class UrlSpec(FieldSpec):


    type: FieldType
    required: bool
    hidden: bool

class FileSpec(FieldSpec):


    type: FieldType
    required: bool
    hidden: bool

class CoordinatesSpec(FieldSpec):


    currentLocation: Optional[bool]

class JsonSpec(FieldSpec):


    type: FieldType
    required: bool
    hidden: bool

class ArrayBooleanSpec(BooleanSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayStringSpec(StringSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayIntegerSpec(IntegerSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayFloatSpec(FloatSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayUrlSpec(UrlSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayFileSpec(FileSpec):


    min_size: Optional[int]
    max_size: Optional[int]

class ArrayCoordinatesSpec(CoordinatesSpec):


    min_size: Optional[int]
    max_size: Optional[int]
