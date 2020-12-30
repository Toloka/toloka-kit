import attr
from toloka.client import structure, unstructure
from toloka.client.primitives.operators import (
    InclusionOperator, InclusionConditionMixin,
    IdentityOperator, IdentityConditionMixin,
    CompareOperator, ComparableConditionMixin,
    # ComparableConditionMixin
)


def test_inclusion_condition_metaclass():

    @attr.attrs(auto_attribs=True)
    class InclusionCondition(InclusionConditionMixin):
        value: int

    # Equivalent conditions
    in_condition = InclusionCondition(operator=InclusionOperator.IN, value=123)
    assert in_condition == InclusionCondition.in_(123)

    not_in_condition = InclusionCondition(operator=InclusionOperator.NOT_IN, value=123)
    assert not_in_condition == InclusionCondition.not_in(123)

    # Different values
    assert InclusionCondition.in_(123) != InclusionCondition.in_(321)
    assert InclusionCondition.not_in(123) != InclusionCondition.not_in(321)

    # Different operators
    assert InclusionCondition.in_(123) != InclusionCondition.not_in(123)
    assert InclusionCondition.not_in(123) != InclusionCondition.in_(123)

    # Different everything
    assert InclusionCondition.in_(123) != InclusionCondition.not_in(321)
    assert InclusionCondition.not_in(123) != InclusionCondition.in_(321)

    # Conversions
    assert in_condition == structure({'operator': 'IN', 'value': 123}, InclusionCondition)
    assert not_in_condition == structure({'operator': 'NOT_IN', 'value': 123}, InclusionCondition)
    assert {'operator': 'IN', 'value': 123} == unstructure(in_condition)
    assert {'operator': 'NOT_IN', 'value': 123} == unstructure(not_in_condition)


def test_identity_condition_metaclass():

    @attr.attrs(auto_attribs=True)
    class IdentityCondition(IdentityConditionMixin):
        value: int

    # Equivalent conditions
    eq_condition = IdentityCondition(IdentityOperator.EQ, 123)
    assert eq_condition == IdentityCondition.eq(123) == (IdentityCondition == 123)

    ne_condition = IdentityCondition(IdentityOperator.NE, 123)
    assert ne_condition == IdentityCondition.ne(123) == (IdentityCondition != 123)

    # Different values
    assert (IdentityCondition == 123) != (IdentityCondition == 321)
    assert (IdentityCondition != 123) != (IdentityCondition != 321)

    # Different operators
    assert (IdentityCondition == 123) != (IdentityCondition != 123)
    assert (IdentityCondition != 123) != (IdentityCondition == 123)

    # Different everything
    assert (IdentityCondition == 123) != (IdentityCondition != 321)
    assert (IdentityCondition != 123) != (IdentityCondition == 321)

    # Conversions
    assert eq_condition == structure({'operator': 'EQ', 'value': 123}, IdentityCondition)
    assert ne_condition == structure({'operator': 'NE', 'value': 123}, IdentityCondition)
    assert {'operator': 'EQ', 'value': 123} == unstructure(eq_condition)
    assert {'operator': 'NE', 'value': 123} == unstructure(ne_condition)


def test_comparable_condition_metaclass():

    class ComparationCondition(ComparableConditionMixin):
        value: int

    # Equivalent conditions
    eq_condition = ComparationCondition(CompareOperator.EQ, 123)
    assert eq_condition == ComparationCondition.eq(123) == (ComparationCondition == 123)

    ne_condition = ComparationCondition(CompareOperator.NE, 123)
    assert ne_condition == ComparationCondition.ne(123) == (ComparationCondition != 123)

    lt_condition = ComparationCondition(CompareOperator.LT, 123)
    assert lt_condition == ComparationCondition.lt(123) == (ComparationCondition < 123)

    gt_condition = ComparationCondition(CompareOperator.GT, 123)
    assert gt_condition == ComparationCondition.gt(123) == (ComparationCondition > 123)

    lte_condition = ComparationCondition(CompareOperator.LTE, 123)
    assert lte_condition == ComparationCondition.lte(123) == (ComparationCondition <= 123)

    gte_condition = ComparationCondition(CompareOperator.GTE, 123)
    assert gte_condition == ComparationCondition.gte(123) == (ComparationCondition >= 123)

    # Different values
    for operator in CompareOperator:
        assert ComparationCondition(operator, 123) != ComparationCondition(operator, 321)

    # Different operators
    for operator_a in CompareOperator:
        for operator_b in CompareOperator:
            if operator_a != operator_b:
                comparison_a = ComparationCondition(operator_a, 123)
                comparison_b = ComparationCondition(operator_b, 123)
                comparison_c = ComparationCondition(operator_b, 321)
                # Same values
                assert comparison_a != comparison_b
                # Different values
                assert comparison_a != comparison_c

    # Conversions
    assert {'operator': 'EQ', 'value': 123} == unstructure(eq_condition)
    assert {'operator': 'NE', 'value': 123} == unstructure(ne_condition)
    assert {'operator': 'LT', 'value': 123} == unstructure(lt_condition)
    assert {'operator': 'GT', 'value': 123} == unstructure(gt_condition)
    assert {'operator': 'LTE', 'value': 123} == unstructure(lte_condition)
    assert {'operator': 'GTE', 'value': 123} == unstructure(gte_condition)
    assert eq_condition == structure({'operator': 'EQ', 'value': 123}, ComparationCondition)
    assert ne_condition == structure({'operator': 'NE', 'value': 123}, ComparationCondition)
    assert lt_condition == structure({'operator': 'LT', 'value': 123}, ComparationCondition)
    assert gt_condition == structure({'operator': 'GT', 'value': 123}, ComparationCondition)
    assert lte_condition == structure({'operator': 'LTE', 'value': 123}, ComparationCondition)
    assert gte_condition == structure({'operator': 'GTE', 'value': 123}, ComparationCondition)


# TODO: implement
# def test_comparable_condition_mixin():
#     pass
