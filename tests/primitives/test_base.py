import pytest
import pickle
import inspect
from toloka.client.primitives.base import BaseTolokaObject
from toloka.util._codegen import attribute
from ..utils.test_extendable_enum import test_enum, test_extendable_enum  # noqa: F401
from typing import Optional, List, Union


@pytest.fixture()
def base_toloka_object():
    obj = BaseTolokaObject()
    obj._unexpected = {'unknown_field': 'unknown_value'}
    return obj


def test_base_toloka_object_is_pickle_serializable(base_toloka_object):
    deserialized = pickle.loads(pickle.dumps(base_toloka_object))
    assert deserialized == base_toloka_object


@pytest.fixture
def toloka_object_with_enum_fields(test_enum, test_extendable_enum):  # noqa: F811

    class MyClass(BaseTolokaObject):
        enum_field: test_enum = attribute(autocast=True, required=True)
        extendable_enum_field: test_extendable_enum = attribute(autocast=True, required=True)

        optional_enum_field: Optional[test_enum] = attribute(autocast=True, required=False)
        optional_extendable_enum_field: Optional[test_extendable_enum] = attribute(autocast=True, required=False)

        complex_enum_field: Optional[List[test_enum]] = attribute(autocast=True, required=False)
        complex_extendable_enum_field: Optional[List[test_extendable_enum]] = attribute(autocast=True, required=False)

    return MyClass


def test_convert_enum(test_enum, test_extendable_enum, toloka_object_with_enum_fields):  # noqa: F811
    toloka_object = toloka_object_with_enum_fields(enum_field='a', extendable_enum_field='c')
    assert toloka_object.optional_enum_field is None and toloka_object.optional_extendable_enum_field is None

    toloka_object.optional_enum_field = 'a'
    toloka_object.optional_extendable_enum_field = 'b'
    assert toloka_object.optional_enum_field == test_enum.A and\
           toloka_object.optional_extendable_enum_field == test_extendable_enum.B

    toloka_object.optional_extendable_enum_field = 'c'
    assert toloka_object.optional_extendable_enum_field == test_extendable_enum.c

    assert toloka_object.enum_field == test_enum.A and toloka_object.extendable_enum_field == test_extendable_enum.c

    toloka_object.enum_field = 'b'
    toloka_object.extendable_enum_field = 'z'
    assert toloka_object.enum_field == test_enum.B and toloka_object.extendable_enum_field == test_extendable_enum.z


def test_converted_enum_has_right_annotation(test_enum, test_extendable_enum, toloka_object_with_enum_fields):  # noqa: F811
    init_signature = inspect.signature(toloka_object_with_enum_fields.__init__)
    assert init_signature.parameters['enum_field'].annotation == Union[test_enum, str]
    assert init_signature.parameters['extendable_enum_field'].annotation == Union[test_extendable_enum, str]
    assert init_signature.parameters['optional_enum_field'].annotation == Union[test_enum, str, None]
    assert init_signature.parameters['optional_extendable_enum_field'].annotation == \
           Union[test_extendable_enum, str, None]

    assert init_signature.parameters['complex_enum_field'].annotation == \
           Optional[List[Union[test_enum, str]]]
    assert init_signature.parameters['complex_extendable_enum_field'].annotation == \
           Optional[List[Union[test_extendable_enum, str]]]
