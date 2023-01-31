from enum import Enum, unique
from typing import Any, Optional

import pytest
from toloka.client._converter import converter
from toloka.client.primitives.base import BaseTolokaObject


@unique
class ItemType(Enum):
    LIST = 'list'
    SET = 'set'


@unique
class SetMethod(Enum):
    POP = 'pop'


class MethodCall(BaseTolokaObject, spec_enum=ItemType, spec_field='type'):
    pass


class SetMethodCall(MethodCall, spec_value=ItemType.SET, spec_enum=SetMethod, spec_field='method'):
    pass


class SetPopMethodCall(SetMethodCall, spec_value=SetMethod.POP):
    pass


class ListMethodCall(MethodCall, spec_value=ItemType.LIST, spec_enum='Method', spec_field='method'):

    @unique
    class Method(Enum):
        APPEND = 'append'
        POP = 'pop'

    APPEND = Method.APPEND
    POP = Method.POP


class ListAppendMethodCall(ListMethodCall, spec_value=ListMethodCall.APPEND):
    argument: Any


class ListPopMethodCallDummyBase(ListMethodCall):
    pass


class ListPopMethodCall(ListPopMethodCallDummyBase, spec_value=ListMethodCall.POP):
    argument: Optional[int] = None


def test_class_attributes():
    assert not hasattr(MethodCall, 'type')
    assert not hasattr(MethodCall, 'method')

    assert SetMethodCall.type == ItemType.SET
    assert ListMethodCall.type == ItemType.LIST
    assert ListPopMethodCallDummyBase.type == ItemType.LIST
    assert not hasattr(SetMethodCall, 'method')
    assert not hasattr(ListMethodCall, 'method')
    assert not hasattr(ListPopMethodCallDummyBase, 'method')

    assert SetPopMethodCall.type == ItemType.SET
    assert SetPopMethodCall.method == SetMethod.POP
    assert ListPopMethodCall.type == ItemType.LIST
    assert ListPopMethodCall.method == ListMethodCall.Method.POP
    assert ListAppendMethodCall.type == ItemType.LIST
    assert ListAppendMethodCall.method == ListMethodCall.Method.APPEND


def test_structure_variant():
    assert SetPopMethodCall() == converter.structure({'type': 'set', 'method': 'pop'}, MethodCall)
    assert ListPopMethodCall() == converter.structure({'type': 'list', 'method': 'pop'}, MethodCall)
    assert ListPopMethodCall(argument=-1) == converter.structure({'type': 'list', 'method': 'pop', 'argument': -1}, MethodCall)
    assert ListAppendMethodCall(argument='abc') == converter.structure(
        {'type': 'list', 'method': 'append', 'argument': 'abc'},
        MethodCall
    )

    with pytest.raises(TypeError):
        converter.structure({'method': 'pop'})
    with pytest.raises(TypeError):
        converter.structure({'type', 'set'})
    with pytest.raises(TypeError):
        converter.structure({'type': 'set', 'method': 'append'})
    with pytest.raises(TypeError):
        converter.structure({'type': 'list', 'method': 'append'})
    with pytest.raises(TypeError):
        converter.structure({'type': 'list', 'method': 'pop', 'argument': 'abc'})


def test_structure_unknown_variant():
    unstructured_with_unknown_high_level_variant = {'type':  'dict', 'method': 'pop'}
    unstructured_with_unknown_low_level_variant = {'type': 'list', 'method': 'index'}
    unstructured_with_unknown_both_levels_variants = {'type': 'dict', 'method': 'get'}

    method_call_with_unknown_high_level_variant = converter.structure(unstructured_with_unknown_high_level_variant,
                                                                      MethodCall)
    method_call_with_unknown_low_level_variant = converter.structure(unstructured_with_unknown_low_level_variant,
                                                                     MethodCall)
    method_call_with_unknown_both_levels_variants = converter.structure(unstructured_with_unknown_both_levels_variants,
                                                                        MethodCall)

    assert MethodCall._variant_registry['_unknown_variant'](**unstructured_with_unknown_high_level_variant) \
           == method_call_with_unknown_high_level_variant
    assert ListMethodCall._variant_registry['_unknown_variant'](method='index') \
           == method_call_with_unknown_low_level_variant
    assert MethodCall._variant_registry['_unknown_variant'](**unstructured_with_unknown_both_levels_variants) == \
           method_call_with_unknown_both_levels_variants

    assert converter.unstructure(
        method_call_with_unknown_high_level_variant) == unstructured_with_unknown_high_level_variant
    assert converter.unstructure(
        method_call_with_unknown_low_level_variant) == unstructured_with_unknown_low_level_variant
    assert converter.unstructure(
        method_call_with_unknown_both_levels_variants) == unstructured_with_unknown_both_levels_variants


def test_unstructure_variant():
    assert {'type': 'set', 'method': 'pop'} == converter.unstructure(SetPopMethodCall())
    assert {'type': 'list', 'method': 'pop'} == converter.unstructure(ListPopMethodCall())
    assert {'type': 'list', 'method': 'pop', 'argument': -1} == converter.unstructure(ListPopMethodCall(argument=-1))
    assert {'type': 'list', 'method': 'append', 'argument': 'abc'} == converter.unstructure(ListAppendMethodCall(argument='abc'))
