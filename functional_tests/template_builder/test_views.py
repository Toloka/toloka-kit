import pytest
import functools

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def action_button_view(notify_action, add_label_hint_validation):
    return add_label_hint_validation(tb.ActionButtonViewV1)(
        notify_action,
    )


@pytest.fixture(params=[e.value for e in tb.AlertViewV1.Theme])
def alert_view(request, text_view, add_label_hint_validation):
    return add_label_hint_validation(tb.AlertViewV1)(
        text_view,
        theme=request.param,
    )


@pytest.fixture
def audio_view(add_label_hint_validation):
    return add_label_hint_validation(tb.AudioViewV1)(
        'http://fake-url',
        loop=True,
    )


@pytest.fixture
def collapse_view(text_view, add_label_hint_validation):
    return add_label_hint_validation(tb.CollapseViewV1)(
        text_view,
        default_opened=True,
    )


@pytest.fixture
def partial_device_frame_view(text_view, add_label_hint_validation):
    return functools.partial(
        add_label_hint_validation(tb.DeviceFrameViewV1),
        text_view,
        max_width=500.,
        min_width=300.
    )


@pytest.fixture
def device_frame_view(partial_device_frame_view):
    return partial_device_frame_view(ratio=[1., 2.])


@pytest.fixture
def device_frame_view_full_height(partial_device_frame_view):
    return partial_device_frame_view(full_height=True)


@pytest.fixture
def divider_view(add_label_hint_validation):
    return add_label_hint_validation(tb.DividerViewV1)()


@pytest.fixture
def group_view(text_view, add_label_hint_validation):
    return add_label_hint_validation(tb.GroupViewV1)(text_view)


@pytest.fixture
def partial_iframe_view(add_label_hint_validation):
    return functools.partial(
        add_label_hint_validation(tb.IframeViewV1),
        'http://fake-url',
        max_width=500.,
        min_width=300.,
    )


@pytest.fixture
def iframe_view(partial_iframe_view):
    return partial_iframe_view(ratio=[1., 2.])


@pytest.fixture
def iframe_view_full_height(partial_iframe_view):
    return partial_iframe_view(full_height=True)


@pytest.fixture
def partial_image_view(add_label_hint_validation):
    return functools.partial(
        add_label_hint_validation(tb.ImageViewV1),
        'http://fake-url',
        max_width=500.,
        min_width=300.,
        no_border=False,
        no_lazy_load=True,
        popup=False,
        rotatable=True,
        scrollable=True,
    )


@pytest.fixture
def image_view(partial_image_view):
    return partial_image_view(ratio=[1., 2.])


@pytest.fixture
def image_view_full_height(partial_image_view):
    return partial_image_view(full_height=True)


@pytest.fixture
def labeled_list_view(text_view, add_label_hint_validation):
    return add_label_hint_validation(tb.LabeledListViewV1)(
        [
            tb.LabeledListViewV1.Item(
                text_view,
                'label',
                center_label=True,
                hint='hint',
            ),
            tb.LabeledListViewV1.Item(
                text_view,
                'label',
                center_label=True,
                hint='hint',
            )
        ],
        min_width=300.,
    )


@pytest.fixture
def link_view(add_label_hint_validation):
    return add_label_hint_validation(tb.LinkViewV1)(
        'http://fake-url',
        content='LINK',
    )


@pytest.fixture
def link_group_view(add_label_hint_validation):
    return add_label_hint_validation(tb.LinkGroupViewV1)(
        [
            tb.LinkGroupViewV1.Link(
                'LINK_1',
                'http://fake-url',
                theme='primary'
            ),
            tb.LinkGroupViewV1.Link(
                'http://fake-url'
                'LINK_2',
            )
        ],
    )


@pytest.fixture
def list_view(text_view, add_label_hint_validation):
    return add_label_hint_validation(tb.ListViewV1)(
        [text_view, text_view],
        direction='horizontal',
        size='s',
    )


@pytest.fixture
def markdown_view(add_label_hint_validation):
    return add_label_hint_validation(tb.MarkdownViewV1)(
        '## i am markdown header',
    )


@pytest.fixture
def video_view(add_label_hint_validation):
    return add_label_hint_validation(tb.VideoViewV1)(
        'http://fake-url',
        ratio=[1., 2.],
        min_width=300.,
        max_width=500.,
        full_height=True,
    )


@pytest.mark.parametrize(
    'view_component', [
        lazy_fixture('action_button_view'),
        lazy_fixture('alert_view'),
        lazy_fixture('audio_view'),
        lazy_fixture('collapse_view'),
        lazy_fixture('device_frame_view'),
        lazy_fixture('device_frame_view_full_height'),
        lazy_fixture('divider_view'),
        lazy_fixture('group_view'),
        lazy_fixture('iframe_view'),
        lazy_fixture('iframe_view_full_height'),
        lazy_fixture('image_view'),
        lazy_fixture('image_view_full_height'),
        lazy_fixture('labeled_list_view'),
        lazy_fixture('link_view'),
        lazy_fixture('link_group_view'),
        lazy_fixture('list_view'),
        lazy_fixture('markdown_view'),
        lazy_fixture('text_view'),
        lazy_fixture('video_view'),
    ]
)
def test_view_component(view_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=view_component
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
