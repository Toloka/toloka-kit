import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def input_data():
    return tb.InputData(
        'test_data', 10,
    )


@pytest.fixture
def internal_data():
    return tb.InternalData(
        'test_data', 10,
    )


@pytest.fixture
def local_data():
    return tb.LocalData(
        'test_data', 10,
    )


@pytest.fixture
def location_data():
    return tb.LocationData()


@pytest.fixture
def output_data():
    return tb.OutputData(
        'test_data',
    )


@pytest.fixture
def relative_data():
    return tb.RelativeData(
        'test_data', 10,
    )


@pytest.mark.parametrize(
    'data_component', [
        lazy_fixture('input_data'),
        lazy_fixture('internal_data'),
        lazy_fixture('local_data'),
        lazy_fixture('location_data'),
        lazy_fixture('output_data'),
        lazy_fixture('relative_data'),
    ]
)
def test_data_component(data_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=tb.TextViewV1(
            content='Hello world',
            validation=tb.EmptyConditionV1(
                data=data_component,
            )
        )
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
