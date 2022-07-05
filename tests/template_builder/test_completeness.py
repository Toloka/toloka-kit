import pytest
import requests

from toloka.client.project.template_builder.base import ComponentType


UNDOCUMENTED_COMPONENTS = {
    'action.list-push',
    'action.list-remove',
    'action.set-current-time',
    'action.set-duration',
    'action.set-media-status',
    'action.set-volume',
    'action.web-phone-call',
    'action.web-phone-call-next',
    'action.zoom-in-out',
    'condition.contains',
    'condition.less',
    'condition.more',
    'core',
    'field.bounding-box',
    'field.multi-select',
    'helper.length',
    'helper.sum',
    'view.debug',
    'view.hint',
    'view.json',
    'view.table',
    'view.web-phone',
    'view.web-phone-next',
    'view.with-label',
    'field.button-checkbox',
    'field.map',
    'field.tumbler',
}


def is_component_blacklisted(component):
    return (
        component['type'].startswith('@') and not component['type'].startswith('@yandex-toloka') or
        component['type'].startswith('lib.') or
        component['type'] in UNDOCUMENTED_COMPONENTS
    )


@pytest.fixture
def tb_components_list():
    components = list(
        component for component in requests.get('https://tb.yandex.net/registry2/latest').json()['found']
        if not is_component_blacklisted(component)
    )
    return components


@pytest.fixture
def implemented_tb_classes():
    return set(ct.value for ct in ComponentType)


def test_component_is_implemented(tb_components_list, implemented_tb_classes):
    for tb_component in tb_components_list:
        assert tb_component['type'] in implemented_tb_classes
