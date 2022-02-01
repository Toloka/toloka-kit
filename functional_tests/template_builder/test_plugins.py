import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def image_annotation_hotkeys_plugin(empty_condition):
    return tb.ImageAnnotationHotkeysPluginV1(
        cancel='a',
        confirm='b',
        labels=["Moscow", "Tokyo", "New York"],
        point='c',
        polygon='d',
        rectangle='e',
        select='f',
    )


@pytest.fixture
def text_annotation_hotkeys_plugin():
    return tb.TextAnnotationHotkeysPluginV1(
        ['1', '2', '3'], 'c'
    )


@pytest.fixture
def hotkeys_plugin():
    keys = list('abcdefghijklmnopqrstuvwxyz0123456789') + ['up', 'down']
    return tb.HotkeysPluginV1(**{f'key_{key}': tb.SetActionV1(tb.OutputData('label'), 'cat') for key in keys})


@pytest.fixture
def trigger_plugin(empty_condition):
    return tb.TriggerPluginV1(
        action=tb.SetActionV1(tb.OutputData('label'), 'cat'),
        condition=empty_condition,
        fire_immediately=False,
        on_change_of=tb.InputData('url'),
    )


@pytest.fixture(params=[e.value for e in tb.TolokaPluginV1.TolokaPluginLayout.Kind])
def toloka_plugin(request):
    return tb.TolokaPluginV1(
        request.param,
        task_width=100.,  # kind
        notifications=[
            tb.TextViewV1('notification 1'),
            tb.TextViewV1('notification 2'),
        ]
    )


@pytest.mark.parametrize(
    'plugin_component', [
        lazy_fixture('image_annotation_hotkeys_plugin'),
        lazy_fixture('text_annotation_hotkeys_plugin'),
        lazy_fixture('hotkeys_plugin'),
        lazy_fixture('trigger_plugin'),
        lazy_fixture('toloka_plugin'),
    ]
)
def test_plugin_component(plugin_component, client, empty_project, text_view):
    view_spec = TemplateBuilderViewSpec(
        view=text_view,
        plugins=[plugin_component]
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
