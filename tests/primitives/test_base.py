import pytest
import pickle
import inspect
from toloka.util._codegen import attribute
from toloka.client.primitives.base import BaseTolokaObject, autocast_to_enum
from ..utils.test_extendable_enum import test_enum, test_extendable_enum  # noqa: F401
from typing import Optional, List, Union, Dict


@pytest.fixture()
def base_toloka_object():
    obj = BaseTolokaObject()
    obj._unexpected = {'unknown_field': 'unknown_value'}
    return obj


def test_base_toloka_object_is_pickle_serializable(base_toloka_object):
    deserialized = pickle.loads(pickle.dumps(base_toloka_object))
    assert deserialized == base_toloka_object


@pytest.fixture
def non_attr_class():
    class NonAttrClass:
        def __init__(self, arg):
            self.arg = arg

    return NonAttrClass


@pytest.fixture
def toloka_object_with_enum_fields(test_enum, test_extendable_enum, non_attr_class):  # noqa: F811

    class MyClass(BaseTolokaObject):
        enum_field: test_enum = attribute(autocast=True, required=True)
        extendable_enum_field: test_extendable_enum = attribute(autocast=True, required=True)

        optional_enum_field: Optional[test_enum] = attribute(autocast=True, required=False)
        optional_extendable_enum_field: Optional[test_extendable_enum] = attribute(autocast=True, required=False)

        complex_enum_field: Optional[List[test_enum]] = attribute(autocast=True, required=False)
        complex_extendable_enum_field: Optional[List[test_extendable_enum]] = attribute(autocast=True, required=False)

        union_enum_field: Union[test_enum, non_attr_class] = attribute(autocast=True, required=False)
        union_extendable_enum_field: Union[test_extendable_enum, non_attr_class] =\
            attribute(autocast=True, required=False)

        complex_union_enum_field: Union[List[test_enum], non_attr_class] = \
            attribute(autocast=True, required=False)
        complex_union_extendable_enum_field: Union[List[test_extendable_enum], non_attr_class] = \
            attribute(autocast=True, required=False)

    return MyClass


def test_convert_enum(test_enum, test_extendable_enum, toloka_object_with_enum_fields, non_attr_class):  # noqa: F811
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

    toloka_object.union_enum_field = 'a'
    toloka_object.union_extendable_enum_field = 'z1'
    assert toloka_object.union_enum_field == test_enum.A and\
           toloka_object.union_extendable_enum_field == test_extendable_enum.z1

    toloka_object.union_enum_field = test_enum.A
    toloka_object.union_extendable_enum_field = test_extendable_enum.A
    assert toloka_object.union_enum_field == test_enum.A and \
           toloka_object.union_extendable_enum_field == test_extendable_enum.A

    toloka_object.complex_union_enum_field = ['a', 'b']
    toloka_object.complex_union_extendable_enum_field = ['a', 'z3']
    assert toloka_object.complex_union_enum_field == [test_enum.A, test_enum.B] and \
           toloka_object.complex_union_extendable_enum_field == [test_extendable_enum.A, test_extendable_enum.z3]

    toloka_object.complex_union_enum_field = non_attr_class
    toloka_object.complex_union_extendable_enum_field = non_attr_class
    assert toloka_object.complex_union_enum_field == non_attr_class and \
           toloka_object.complex_union_extendable_enum_field == non_attr_class


def test_converted_enum_has_right_annotation(
    test_enum, test_extendable_enum, toloka_object_with_enum_fields, non_attr_class  # noqa: F811
):
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

    assert init_signature.parameters['union_enum_field'].annotation == Optional[Union[test_enum, str, non_attr_class]]
    assert init_signature.parameters['union_extendable_enum_field'].annotation == \
           Optional[Union[test_extendable_enum, str, non_attr_class]]

    assert init_signature.parameters['complex_union_enum_field'].annotation == \
           Union[List[Union[test_enum, str]], non_attr_class, None]
    assert init_signature.parameters['complex_union_extendable_enum_field'].annotation == \
           Union[List[Union[test_extendable_enum, str]], non_attr_class, None]


@pytest.fixture
def autocast_to_enum_function(non_attr_class, test_enum, test_extendable_enum):  # noqa: F811
    @autocast_to_enum
    def func(
        arg_1: test_enum,
        arg_2: test_extendable_enum,
        arg_3: Optional[test_enum],
        arg_4: Optional[test_extendable_enum],
        arg_5: List[test_enum],
        arg_6: List[test_extendable_enum],
        arg_7: Dict[str, List[test_enum]],
        arg_8: Dict[str, List[test_extendable_enum]],
        arg_9: non_attr_class,
        arg_10: Dict[non_attr_class, test_enum],
        arg_11: Dict[Union[test_enum, non_attr_class], str]
    ):
        return arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, arg_7, arg_8, arg_9, arg_10, arg_11

    return func


def test_autocast_to_enum_decorator_does_not_cast_arguments_when_unneeded(
    test_enum, test_extendable_enum, non_attr_class, autocast_to_enum_function  # noqa: F811
):
    original_arguments = test_enum.A, \
        test_extendable_enum.A,\
        test_enum.A,\
        None,\
        [test_enum.A, test_enum.B],\
        [test_extendable_enum.A, test_extendable_enum.B],\
        {'a': [test_enum.A]},\
        {'a': [test_extendable_enum.A]},\
        non_attr_class(1),\
        {non_attr_class(1): test_enum.A},\
        {non_attr_class(1): 'value', test_enum.A: '10'}

    casted_arguments = autocast_to_enum_function(*original_arguments)
    assert original_arguments == casted_arguments


def test_autocast_to_enum_decorator_casts_argument(
    test_enum, test_extendable_enum, non_attr_class, autocast_to_enum_function  # noqa: F811
):
    non_attr_class_instance = non_attr_class(1)
    casted_arguments = autocast_to_enum_function(
        'a', 'extended_field', 'a', 'b', ['a', 'b'], ['a', 'extended_field_2'],
        {'a': ['a']}, {'extended_field_3': ['extended_field_3']},
        non_attr_class_instance, {non_attr_class_instance: 'a'},
        {non_attr_class_instance: 'value', 'a': '10'})

    expected_arguments = test_enum.A, \
        test_extendable_enum.extended_field, \
        test_enum.A, \
        test_extendable_enum.B, \
        [test_enum.A, test_enum.B], \
        [test_extendable_enum.A, test_extendable_enum.extended_field_2], \
        {'a': [test_enum.A]}, \
        {'extended_field_3': [test_extendable_enum.extended_field_3]}, \
        non_attr_class_instance, \
        {non_attr_class_instance: test_enum.A}, \
        {non_attr_class_instance: 'value', test_enum.A: '10'}

    assert casted_arguments == expected_arguments


def test_autocast_to_enum_decorator_annotations(
    test_enum, test_extendable_enum, non_attr_class, autocast_to_enum_function  # noqa: F811
):

    expected_annotations = [
        Union[str, test_enum],
        Union[str, test_extendable_enum],
        Union[str, test_enum, None],
        Union[str, test_extendable_enum, None],
        List[Union[str, test_enum]],
        List[Union[str, test_extendable_enum]],
        Dict[str, List[Union[str, test_enum]]],
        Dict[str, List[Union[str, test_extendable_enum]]],
        non_attr_class,
        Dict[non_attr_class, Union[str, test_enum]],
        Dict[Union[test_enum, str, non_attr_class], str],
    ]

    converted_annotations = [p.annotation for p in inspect.signature(autocast_to_enum_function).parameters.values()]
    assert converted_annotations == expected_annotations


def test_enum_union_autocast(test_enum, non_attr_class):  # noqa: F811
    @autocast_to_enum
    def func(arg: Union[test_enum, non_attr_class, None]):
        return arg

    assert func(None) is None
    assert func('123') == '123'
    assert func('a') == test_enum.A
    assert isinstance(func(non_attr_class(1)), non_attr_class)

    @autocast_to_enum
    def func(arg: Union[List[test_enum], non_attr_class, None]):
        return arg

    assert func(['a', 'b']) == [test_enum.A, test_enum.B]
    non_attr_class_instance = non_attr_class(1)
    assert func(non_attr_class_instance) == non_attr_class_instance


def test_extendable_enum_union_autocast(test_extendable_enum, non_attr_class):  # noqa: F811
    @autocast_to_enum
    def func(arg: Union[test_extendable_enum, non_attr_class, None]):
        return arg

    assert func(None) is None
    assert func('field') == test_extendable_enum.field
    assert func('a') == test_extendable_enum.A
    assert isinstance(func(non_attr_class(1)), non_attr_class)

    @autocast_to_enum
    def func(arg: Union[List[test_extendable_enum], non_attr_class, None]):
        return arg

    assert func(['a', 'b', 'field_2']) == [test_extendable_enum.A, test_extendable_enum.B, test_extendable_enum.field_2]
    non_attr_class_instance = non_attr_class(1)
    assert func(non_attr_class_instance) == non_attr_class_instance
