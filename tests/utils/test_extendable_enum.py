import pytest
from enum import Enum

from toloka.client._converter import converter
from toloka.util._extendable_enum import extend_enum, ExtendableStrEnum
from toloka.client.primitives.base import BaseTolokaObject


@pytest.fixture
def test_enum():
    class TestEnum(Enum):
        A = 'a'
        B = 'b'

    return TestEnum


@pytest.fixture
def test_extendable_enum():
    class TestExtendableEnum(ExtendableStrEnum):
        A = 'a'
        B = 'b'

    return TestExtendableEnum


@pytest.mark.parametrize(
    ['name', 'value', 'is_new'],
    [
        ('A', 'b', False),
        ('C', 'a', False),
        ('C', 'c', True)
    ]
)
def test_extend_enum(test_enum, name, value, is_new):
    enum_len = len(test_enum)
    new_member = extend_enum(test_enum, name, value)
    if is_new:
        assert new_member and new_member.name == name and new_member.value == value
        assert len(test_enum) == enum_len + 1
    else:
        assert new_member and (new_member.name == name or new_member.value == value)
        assert len(test_enum) == enum_len


def test_extendable_str_enum(test_extendable_enum):
    assert test_extendable_enum.A.value == 'a'

    assert test_extendable_enum.C
    assert test_extendable_enum.C.name == 'C'
    assert test_extendable_enum.C.value == 'C'

    # get by value
    assert test_extendable_enum('D')
    assert test_extendable_enum.D.name == 'D'
    assert test_extendable_enum.D.value == 'D'

    assert test_extendable_enum(test_extendable_enum.E)
    assert test_extendable_enum.E.name == 'E'
    assert test_extendable_enum.E.value == 'E'

    # get by name
    assert test_extendable_enum['F']
    assert test_extendable_enum.F.name == 'F'
    assert test_extendable_enum.F.value == 'F'


def test_extendable_str_enum_structure(test_extendable_enum):
    result = converter.structure('a', test_extendable_enum)
    assert result and result.name == 'A' and result.value == 'a'

    result = converter.structure('new_key', test_extendable_enum)
    assert result and result.name == 'new_key' and result.value == 'new_key'


def test_extendable_str_enum_unstructure(test_extendable_enum):
    assert converter.unstructure(test_extendable_enum.A) == 'a'
    assert converter.unstructure(test_extendable_enum.D) == 'D'


def test_variant_type():

    class MyEnum(ExtendableStrEnum):
        DOG = 'dog'
        CAT = 'cat'

    class Animal(BaseTolokaObject, spec_enum=MyEnum, spec_field='type'):
        pass

    class Dog(Animal, spec_value=MyEnum.DOG):
        pass

    class Cat(Animal, spec_value=MyEnum.CAT):
        pass

    assert converter.structure({'type': 'dog'}, Animal) == Dog()
    assert converter.structure({'type': 'cat'}, Animal) == Cat()
    assert Dog().unstructure() == {'type': 'dog'}
    assert Cat().unstructure() == {'type': 'cat'}


def test_empty_structure(test_enum, test_extendable_enum):

    class MyClass(BaseTolokaObject):
        enum_field: test_enum
        extendable_enum_field: test_extendable_enum

    assert MyClass.structure({}) == MyClass()
