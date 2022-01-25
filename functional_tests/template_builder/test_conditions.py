import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def all_condition(empty_condition):
    return tb.AllConditionV1(
        [empty_condition],
        hint='hint'
    )


@pytest.fixture
def any_condition(empty_condition):
    return tb.AnyConditionV1(
        [empty_condition],
        hint='hint'
    )


@pytest.fixture
def distance_condition():
    return tb.DistanceConditionV1(
        'coord0', 'coord1', 100.,
        hint='hint'
    )


@pytest.fixture
def equals_condition():
    return tb.EqualsConditionV1(
        'value', tb.InputData('url'),
        hint='hint'
    )


@pytest.fixture
def link_opened_condition():
    return tb.LinkOpenedConditionV1(
        'http://fake-url',
        hint='hint'
    )


@pytest.fixture
def not_condition(empty_condition):
    return tb.NotConditionV1(
        empty_condition,
        hint='hint'
    )


@pytest.fixture
def played_condition():
    return tb.PlayedConditionV1(
        hint='hint'
    )


@pytest.fixture
def played_fully_condition():
    return tb.PlayedFullyConditionV1(
        hint='hint'
    )


@pytest.fixture
def required_condition():
    return tb.RequiredConditionV1(
        tb.InputData('url'),
        hint='hint'
    )


@pytest.fixture
def same_domain_condition():
    return tb.SameDomainConditionV1(
        tb.InputData('url'),
        'http://fake-url',
        hint='hint'
    )


@pytest.fixture
def schema_condition():
    return tb.SchemaConditionV1(
        tb.InputData('url'),
        # example schema from https://json-schema.org/learn/getting-started-step-by-step.html
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://example.com/product.schema.json",
            "title": "Product",
            "description": "A product in the catalog",
            "type": "object"
        },
        hint='hint'
    )


@pytest.fixture
def sub_array_condition():
    return tb.SubArrayConditionV1(
        ['http://fake-url'],
        tb.InputData('url'),
        hint='hint'
    )


@pytest.mark.parametrize(
    'condition_component', [
        lazy_fixture('any_condition'),
        lazy_fixture('all_condition'),
        lazy_fixture('distance_condition'),
        lazy_fixture('empty_condition'),
        lazy_fixture('equals_condition'),
        lazy_fixture('link_opened_condition'),
        lazy_fixture('not_condition'),
        lazy_fixture('played_condition'),
        lazy_fixture('played_fully_condition'),
        lazy_fixture('required_condition'),
        lazy_fixture('same_domain_condition'),
        lazy_fixture('schema_condition'),
        lazy_fixture('sub_array_condition'),
    ]
)
def test_condition_component(condition_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=tb.TextViewV1(
            content='Hello world',
            validation=condition_component,
        )
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
