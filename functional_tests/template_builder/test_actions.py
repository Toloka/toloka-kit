import pytest

from . import assert_view_spec_uploads_to_project
from pytest_lazyfixture import lazy_fixture
from toloka.client.project import TemplateBuilderViewSpec
from toloka.client.project import template_builder as tb


@pytest.fixture
def bulk_action(notify_action):
    return tb.BulkActionV1(notify_action)


@pytest.fixture
def open_close_action():
    return tb.OpenCloseActionV1(
        tb.base.RefComponent('fake_ref')
    )


@pytest.fixture
def open_link_action():
    return tb.OpenLinkActionV1(
        'http://fake_url'
    )


@pytest.fixture
def play_pause_action():
    return tb.PlayPauseActionV1(
        tb.base.RefComponent('fake_ref')
    )


@pytest.fixture(params=[e.value for e in tb.RotateActionV1.Payload])
def rotate_action(request):
    return tb.RotateActionV1(
        tb.base.RefComponent('fake_ref'),
        request.param  # payload
    )


@pytest.fixture
def set_action():
    return tb.SetActionV1(
        tb.OutputData('label'), True
    )


@pytest.fixture
def toggle_action():
    return tb.ToggleActionV1(
        tb.OutputData('label')
    )


@pytest.mark.parametrize(
    'action_component', [
        lazy_fixture('bulk_action'),
        lazy_fixture('notify_action'),
        lazy_fixture('open_close_action'),
        lazy_fixture('open_link_action'),
        lazy_fixture('play_pause_action'),
        lazy_fixture('rotate_action'),
        lazy_fixture('set_action'),
        lazy_fixture('toggle_action'),
    ]
)
def test_action_component(action_component, client, empty_project):
    view_spec = TemplateBuilderViewSpec(
        view=tb.ActionButtonViewV1(
            action=action_component
        )
    )
    assert_view_spec_uploads_to_project(
        client, empty_project, view_spec
    )
