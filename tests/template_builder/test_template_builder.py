import pytest
import json

from toloka.client.project.view_spec import ViewSpec
from toloka.client.project.template_builder import TemplateBuilder
from toloka.client.project.template_builder.actions import SetActionV1
from toloka.client.project.template_builder.base import RefComponent
from toloka.client.project.template_builder.conditions import RequiredConditionV1
from toloka.client.project.template_builder.data import OutputData, InputData
from toloka.client.project.template_builder.fields import RadioGroupFieldV1, TextareaFieldV1, GroupFieldOption
from toloka.client.project.template_builder.layouts import SideBySideLayoutV1
from toloka.client.project.template_builder.plugins import HotkeysPluginV1
from toloka.client.project.template_builder.view import ListViewV1, ImageViewV1


@pytest.fixture
def view_spec_map():
    return {
        'settings': {
            'resolution': 1024,
        },
        'type': 'tb',
        'config': json.dumps({
            "vars": {
                "0": {
                    "type": "data.output",
                    "path": "result"
                }
            },
            "plugins": [
                {
                    "0": {
                        "type": "action.set",
                        "data": {
                            "$ref": "vars.0"
                        },
                        "payload": "failure"
                    },
                    "1": {
                        "type": "action.set",
                        "data": {
                            "$ref": "vars.0"
                        },
                        "payload": "a"
                    },
                    "2": {
                        "type": "action.set",
                        "data": {
                            "$ref": "vars.0"
                        },
                        "payload": "b"
                    },
                    "type": "plugin.hotkeys"
                }
            ],
            "view": {
                "type": "layout.side-by-side",
                "items": [
                    {
                        "type": "view.image",
                        "url": {
                            "type": "data.input",
                            "path": "image_a"
                        },
                        "fullHeight": True
                    },
                    {
                        "type": "view.image",
                        "url": {
                            "type": "data.input",
                            "path": "image_b"
                        },
                        "fullHeight": True
                    }
                ],
                "controls": {
                    "type": "view.list",
                    "items": [
                        {
                            "type": "field.radio-group",
                            "label": "Какое фото вам больше нравится?",
                            "options": [
                                {
                                    "label": "A",
                                    "value": "a"
                                },
                                {
                                    "label": "B",
                                    "value": "b",
                                    "hint": {
                                        "type": "field.textarea",
                                        "data": {
                                            "type": "data.input",
                                            "path": "text"
                                        }
                                    }
                                },
                                {
                                    "label": "Картинки не загрузились",
                                    "value": "failure"
                                }
                            ],
                            "data": {
                                "$ref": "vars.0"
                            }
                        },
                        {
                            "type": "field.textarea",
                            "label": {
                                "type": "data.input",
                                "path": "text"
                            },
                            "data": {
                                "type": "data.output",
                                "path": "why"
                            },
                            "validation": {
                                "type": "condition.required"
                            }
                        }
                    ]
                }
            }
        }),
        "lock": {
            'core': '1.0.0',
            'condition.required': '1.0.0',
            'field.textarea': '1.0.0',
            'field.radio-group': '1.0.0',
            'view.list': '1.0.0',
            'view.image': '1.2.3',
            'layout.side-by-side': '1.0.0',
            'plugin.hotkeys': '1.0.0',
            'action.set': '1.0.0',
        }
    }


def test_result(view_spec_map):
    expected_result = TemplateBuilder(
        view=SideBySideLayoutV1(
            version='1.0.0',
            controls=ListViewV1(
                version='1.0.0',
                items=[
                    RadioGroupFieldV1(
                        version='1.0.0',
                        data=RefComponent(
                            ref='vars.0'
                        ),
                        label='Какое фото вам больше нравится?',
                        options=[
                            GroupFieldOption(
                                label='A',
                                value='a'
                            ),
                            GroupFieldOption(
                                label='B',
                                value='b',
                                hint=TextareaFieldV1(
                                    data=InputData(
                                        path='text'
                                    ),
                                    version='1.0.0'
                                )
                            ),
                            GroupFieldOption(
                                label='Картинки не загрузились',
                                value='failure'
                            )
                        ],
                    ),
                    TextareaFieldV1(
                        version='1.0.0',
                        data=OutputData(
                            path='why'
                        ),
                        label=InputData(
                            path='text'
                        ),
                        validation=RequiredConditionV1(
                            version='1.0.0'
                        )
                    )
                ]
            ),
            items=[
                ImageViewV1(
                    version='1.2.3',
                    url=InputData(
                        path='image_a',
                    ),
                    full_height=True
                ),
                ImageViewV1(
                    version='1.2.3',
                    url=InputData(
                        path='image_b'
                    ),
                    full_height=True
                )
            ]
        ),
        plugins=[
            HotkeysPluginV1(
                version='1.0.0',
                key_0=SetActionV1(
                    version='1.0.0',
                    data=RefComponent(ref='vars.0'),
                    payload='failure'
                ),
                key_1=SetActionV1(
                    version='1.0.0',
                    data=RefComponent(ref='vars.0'),
                    payload='a'
                ),
                key_2=SetActionV1(
                    version='1.0.0',
                    data=RefComponent(ref='vars.0'),
                    payload='b'
                )
            )
        ],
        vars={'0': OutputData(path='result')}
    )

    result = ViewSpec.structure(view_spec_map)
    assert result.config == expected_result


def test_ref(view_spec_map):
    result = ViewSpec.structure(view_spec_map)
    assert result.config.plugins[0].key_0.data == RefComponent(ref='vars.0')


def test_union_with_base_component_parsing(view_spec_map):
    result = ViewSpec.structure(view_spec_map)
    assert result.config.vars['0'] == OutputData(path='result')
    assert result.config.view.controls.items[1].label == InputData(path='text')


def test_versions(view_spec_map):
    result = ViewSpec.structure(view_spec_map)
    assert result.config.view.items[0].version == '1.2.3'


@pytest.mark.parametrize('new_version', ('2.2.3', '1.1.3', '1.2.0'))
def test_inconsistent_versions(view_spec_map, new_version):
    result = ViewSpec.structure(view_spec_map)
    if new_version.startswith('1.'):
        result.config.view.items[0].version = new_version
        with pytest.raises(RuntimeError) as excinfo:
            result.unstructure()
        assert excinfo.value.args[0] == 'Different versions of the same component: view.image'
    else:
        with pytest.raises(ValueError) as excinfo:
            result.config.view.items[0].version = new_version
        assert excinfo.value.args[0] == 'only v1 components are supported'
