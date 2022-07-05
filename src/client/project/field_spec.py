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
from enum import unique
from typing import List

from ..primitives.base import BaseTolokaObject
from ...util._docstrings import inherit_docstrings
from ...util._extendable_enum import ExtendableStrEnum


@unique
class FieldType(ExtendableStrEnum):
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
    for input and response data validation specification respectively. Use subclasses of this
    class defined below to define the data type (string, integer, URL, etc.) and specify
    validation parameters (such as string length).

    Attributes:
        required: Whether the object or input field is required.
        hidden: Whether to hide the input field from Tolokers.
    """
    required: bool = True
    hidden: bool = False


@inherit_docstrings
class BooleanSpec(FieldSpec, spec_value=FieldType.BOOLEAN):
    """A boolean field specification

    Attributes:
        allowed_values: Allowed values
    """
    allowed_values: List[bool]


@inherit_docstrings
class StringSpec(FieldSpec, spec_value=FieldType.STRING):
    """A string field specification

    Attributes:
        min_length: Minimum length of the string
        max_length: Maximum length of the string
        allowed_values: Allowed values
    """
    min_length: int
    max_length: int
    allowed_values: List[str]


@inherit_docstrings
class IntegerSpec(FieldSpec, spec_value=FieldType.INTEGER):
    """An integer field specification

    Attributes:
        min_value: Minimum value of the number
        max_value: Maximum value of the number
        allowed_values: Allowed values
    """
    min_value: int
    max_value: int
    allowed_values: List[int]


@inherit_docstrings
class FloatSpec(FieldSpec, spec_value=FieldType.FLOAT):
    """An floating point field specification

    Attributes:
        min_value: Minimum value of the number
        max_value: Maximum value of the number
    """
    min_value: float
    max_value: float


@inherit_docstrings
class UrlSpec(FieldSpec, spec_value=FieldType.URL):
    """A url field specification
    """


@inherit_docstrings
class FileSpec(FieldSpec, spec_value=FieldType.FILE):
    """A file field specification (only for output data)
    """


@inherit_docstrings
class CoordinatesSpec(FieldSpec, spec_value=FieldType.COORDINATES):
    """Geographical coordinates field specification, such as “53.910236,27.531110

    Attributes:
        current_location: put the Toloker's current coordinates in the field (true/false).
            Used in tasks for the mobile app.
    """
    current_location: bool


@inherit_docstrings
class JsonSpec(FieldSpec, spec_value=FieldType.JSON):
    """A JSON object field specification
    """


@inherit_docstrings
class ArrayBooleanSpec(BooleanSpec, spec_value=FieldType.ARRAY_BOOLEAN):
    """A boolean array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayStringSpec(StringSpec, spec_value=FieldType.ARRAY_STRING):
    """A string array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayIntegerSpec(IntegerSpec, spec_value=FieldType.ARRAY_INTEGER):
    """An integer array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayFloatSpec(FloatSpec, spec_value=FieldType.ARRAY_FLOAT):
    """An floating point array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayUrlSpec(UrlSpec, spec_value=FieldType.ARRAY_URL):
    """A url array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayFileSpec(FileSpec, spec_value=FieldType.ARRAY_FILE):
    """A file array field specification (only for output data)

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayCoordinatesSpec(CoordinatesSpec, spec_value=FieldType.ARRAY_COORDINATES):
    """Geographical coordinates array field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int


@inherit_docstrings
class ArrayJsonSpec(JsonSpec, spec_value=FieldType.ARRAY_JSON):
    """A JSON object field specification

    Attributes:
        min_size: Minimum number of elements in the array
        max_size: Maximum number of elements in the array
    """
    min_size: int
    max_size: int
