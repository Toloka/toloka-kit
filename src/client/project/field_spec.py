__all__ = [
    'FieldType',
    'FieldSpec',
    'BooleanSpec',
    'StringSpec',
    'IntegerSpec',
    'FloatSpec',
    'UrlSpec',
    'FileSpec',
    'CoordinatesSpec',
    'JsonSpec',
    'ArrayBooleanSpec',
    'ArrayStringSpec',
    'ArrayIntegerSpec',
    'ArrayFloatSpec',
    'ArrayUrlSpec',
    'ArrayFileSpec',
    'ArrayCoordinatesSpec'
]
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
    """A base class for field specifications used in project's `input_spec` and `output_spec`
    for input and respose data validation specification respectively. Use subclasses of this
    class defined below to define the data type (string, integer, URL, etc.) and specify
    validation parameters (such as string length).

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
    """
    required: bool = True
    hidden: bool = False


class BooleanSpec(FieldSpec, spec_value=FieldType.BOOLEAN):
    """A boolean field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        allowed_values: Allowed values
    """
    allowed_values: List[bool]


class StringSpec(FieldSpec, spec_value=FieldType.STRING):
    """A string field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        allowed_values: Allowed values
    """
    min_length: int
    max_length: int
    allowed_values: List[str]


class IntegerSpec(FieldSpec, spec_value=FieldType.INTEGER):
    """An integer field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        allowed_values: Allowed values
    """
    min_value: int
    max_value: int
    allowed_values: List[int]


class FloatSpec(FieldSpec, spec_value=FieldType.FLOAT):
    """An floating point field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_value: Minimum value of the number
        max_value: Maximum value of the number
    """
    min_value: float
    max_value: float


class UrlSpec(FieldSpec, spec_value=FieldType.URL):
    """A url field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
    """


class FileSpec(FieldSpec, spec_value=FieldType.FILE):
    """A file field specification (only for output data)

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
    """


class CoordinatesSpec(FieldSpec, spec_value=FieldType.COORDINATES):
    """Geographical coordinates field specification, such as “53.910236,27.531110

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        current_location: put the user's current coordinates in the field (true/false).
            Used in tasks for the mobile app.
    """
    current_location: bool


class JsonSpec(FieldSpec, spec_value=FieldType.JSON):
    """A JSON object field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
    """


class ArrayBooleanSpec(BooleanSpec, spec_value=FieldType.ARRAY_BOOLEAN):
    """A boolean array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayStringSpec(StringSpec, spec_value=FieldType.ARRAY_STRING):
    """A string array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayIntegerSpec(IntegerSpec, spec_value=FieldType.ARRAY_INTEGER):
    """An integer array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        allowed_values: Allowed values
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayFloatSpec(FloatSpec, spec_value=FieldType.ARRAY_FLOAT):
    """An floating point array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayUrlSpec(UrlSpec, spec_value=FieldType.ARRAY_URL):
    """A url array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayFileSpec(FileSpec, spec_value=FieldType.ARRAY_FILE):
    """A file array field specification (only for output data)

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


class ArrayCoordinatesSpec(CoordinatesSpec, spec_value=FieldType.ARRAY_COORDINATES):
    """Geographical coordinates array field specification

    Attributes:
        required: Whether the object or input field is required
        hidden: Whether or not to hide the input value field from the user
        current_location: put the user's current coordinates in the field (true/false).
            Used in tasks for the mobile app
        min_size: Minimum number of elements in the array
        min_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int
