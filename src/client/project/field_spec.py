from enum import Enum, unique
from typing import List

from ..primitives.base import BaseTolokaObject


@unique
class FieldType(Enum):
    BOOLEAN = 'boolean'
    STRING = 'string'
    FLOAT = 'float'
    INTEGER = 'integer'
    URL = 'url'
    FILE = 'file'
    COORDINATES = 'coordinates'
    JSON = 'json'

    ARRAY_BOOLEAN = 'array_boolean'
    ARRAY_STRING = 'array_string'
    ARRAY_INTEGER = 'array_integer'
    ARRAY_FLOAT = 'array_float'
    ARRAY_URL = 'array_url'
    ARRAY_FILE = 'array_file'
    ARRAY_COORDINATES = 'array_coordinates'
    ARRAY_JSON = 'array_json'


class FieldSpec(BaseTolokaObject, spec_enum=FieldType, spec_field='type'):
    required: bool = True
    hidden: bool = False


class BooleanSpec(FieldSpec, spec_value=FieldType.BOOLEAN):
    allowed_values: List[bool]


class StringSpec(FieldSpec, spec_value=FieldType.STRING):
    min_length: int
    max_length: int
    allowed_values: List[str]


class IntegerSpec(FieldSpec, spec_value=FieldType.INTEGER):
    min_value: int
    max_value: int
    allowed_values: List[int]


class FloatSpec(FieldSpec, spec_value=FieldType.FLOAT):
    min_value: float
    max_value: float


class UrlSpec(FieldSpec, spec_value=FieldType.URL):
    pass


class FileSpec(FieldSpec, spec_value=FieldType.FILE):
    pass


class CoordinatesSpec(FieldSpec, spec_value=FieldType.COORDINATES):
    currentLocation: bool


class JsonSpec(FieldSpec, spec_value=FieldType.JSON):
    pass


class ArrayBooleanSpec(BooleanSpec, spec_value=FieldType.ARRAY_BOOLEAN):
    min_size: int
    max_size: int


class ArrayStringSpec(StringSpec, spec_value=FieldType.ARRAY_STRING):
    min_size: int
    max_size: int


class ArrayIntegerSpec(IntegerSpec, spec_value=FieldType.ARRAY_INTEGER):
    min_size: int
    max_size: int


class ArrayFloatSpec(FloatSpec, spec_value=FieldType.ARRAY_FLOAT):
    min_size: int
    max_size: int


class ArrayUrlSpec(UrlSpec, spec_value=FieldType.ARRAY_URL):
    min_size: int
    max_size: int


class ArrayFileSpec(FileSpec, spec_value=FieldType.ARRAY_FILE):
    min_size: int
    max_size: int


class ArrayCoordinatesSpec(CoordinatesSpec, spec_value=FieldType.ARRAY_COORDINATES):
    min_size: int
    max_size: int
