import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def concat_arrays_helper():
    return tb.ConcatArraysHelperV1([[1, 2, 3], [4, 5, 6]])


@pytest.fixture
def entries_2_object_helper():
    return tb.Entries2ObjectHelperV1(
        [tb.Entries2ObjectHelperV1.Entry(key='key', value='value')]
    )


@pytest.fixture
def if_helper(empty_condition):
    return tb.IfHelperV1(
        empty_condition,
        tb.TextViewV1('then'),
        else_=tb.TextViewV1('else'),
    )


@pytest.fixture
def join_helper():
    return tb.JoinHelperV1(
        ['Hello', 'world', '!'],
        ' ',
    )


@pytest.fixture
def object_2_entries_helper():
    return tb.Object2EntriesHelperV1(
        {
            'key1': 'value1',
            'key2': 'value2',
        }
    )


@pytest.fixture
def replace_helper():
    return tb.ReplaceHelperV1(
        'ababbaba',
        'ab',
        'c'
    )


@pytest.fixture
def search_query_helper():
    return tb.SearchQueryHelperV1(
        'Toloka',
        'wikipedia',
    )


@pytest.fixture
def switch_helper(empty_condition):
    return tb.SwitchHelperV1(
        [
            tb.SwitchHelperV1.Case(
                condition=empty_condition,
                result=tb.TextViewV1('first')
            ),
            tb.SwitchHelperV1.Case(
                condition=tb.NotConditionV1(condition=empty_condition),
                result=tb.TextViewV1('second')
            )
        ],
        tb.TextViewV1('default')
    )


@pytest.fixture(params=[e.value for e in tb.TextTransformHelperV1.Transformation])
def text_transform_helper(request):
    return tb.TextTransformHelperV1(
        'sample',
        request.param  # transformation
    )


@pytest.fixture
def transform_helper():
    return tb.TransformHelperV1(
        tb.ImageViewV1(
            url=tb.RelativeData('item')
        ),
        tb.InputData('url'),
    )


@pytest.fixture
def translate_helper():
    return tb.TranslateHelperV1(
        'test-key'
    )


@pytest.fixture
def yandex_disk_proxy_helper():
    return tb.YandexDiskProxyHelperV1(
        'fake-proxy/my.file'
    )


@pytest.mark.parametrize(
    'helper_component', [
        lazy_fixture('concat_arrays_helper'),
        lazy_fixture('entries_2_object_helper'),
        lazy_fixture('if_helper'),
        lazy_fixture('join_helper'),
        lazy_fixture('object_2_entries_helper'),
        lazy_fixture('replace_helper'),
        lazy_fixture('search_query_helper'),
        lazy_fixture('switch_helper'),
        lazy_fixture('text_transform_helper'),
        lazy_fixture('transform_helper'),
        lazy_fixture('translate_helper'),
        lazy_fixture('yandex_disk_proxy_helper'),
    ]
)
def test_helper_component(helper_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=tb.TextViewV1(
            content=helper_component
        )
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
