import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def bars_layout(empty_condition):
    return tb.BarsLayoutV1(
        tb.TextViewV1('text_view'),
        bar_before=tb.TextViewV1('i am before bar'),
        bar_after=tb.TextViewV1('i am after bar'),
        validation=empty_condition
    )


@pytest.fixture
def columns_layout(empty_condition):
    return tb.ColumnsLayoutV1(
        [
            tb.TextViewV1('column 1'),
            tb.TextViewV1('column 2'),
        ],
        full_height=True,
        min_width=100.,
        ratio=[1., 2.],
        vertical_align='top',
        validation=empty_condition,
    )


@pytest.fixture
def compare_layout(empty_condition):
    return tb.CompareLayoutV1(
        tb.TextViewV1('this is controls'),
        [
            tb.CompareLayoutItem(
                content=tb.TextViewV1('left'),
                controls=tb.TextViewV1('left_controls'),
            ),
            tb.CompareLayoutItem(
                content=tb.TextViewV1('right'),
                controls=tb.TextViewV1('right_controls'),
            ),
        ],
        min_width=300.,
        wide_common_controls=True,
        validation=empty_condition,
    )


@pytest.fixture
def side_by_side_layout(empty_condition):
    return tb.SideBySideLayoutV1(
        tb.CheckboxFieldV1(
            data=tb.InputData('url')
        ),
        [
            tb.TextViewV1('left'),
            tb.TextViewV1('right'),
        ],
        min_item_width=300.,
        validation=empty_condition
    )


@pytest.fixture
def sidebar_layout(empty_condition):
    return tb.SidebarLayoutV1(
        tb.TextViewV1('this is content'),
        tb.TextViewV1('this is controls'),
        controls_width=300.,
        extra_controls=tb.TextViewV1('this is extra controls'),
        min_width=300.,
        validation=empty_condition,
    )


@pytest.mark.parametrize(
    'layout_component', [
        lazy_fixture('bars_layout'),
        lazy_fixture('columns_layout'),
        lazy_fixture('compare_layout'),
        lazy_fixture('side_by_side_layout'),
        lazy_fixture('sidebar_layout'),
    ]
)
def test_layout_component(layout_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=layout_component
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
