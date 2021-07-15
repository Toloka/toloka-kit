import pytest
import json

from toloka.client.project.field_spec import JsonSpec
from toloka.client.project.view_spec import ViewSpec
from toloka.client.project.template_builder import TemplateBuilder, get_input_and_output
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
            ListViewV1(
                [
                    RadioGroupFieldV1(
                        RefComponent(
                            'vars.0'
                        ),
                        [
                            GroupFieldOption(
                                'a',
                                'A',
                            ),
                            GroupFieldOption(
                                'b',
                                'B',
                                hint=TextareaFieldV1(
                                    data=InputData(
                                        'text'
                                    ),
                                    version='1.0.0'
                                )
                            ),
                            GroupFieldOption(
                                'failure',
                                'Картинки не загрузились',
                            )
                        ],
                        label='Какое фото вам больше нравится?',
                        version='1.0.0'
                    ),
                    TextareaFieldV1(
                        OutputData(
                            'why'
                        ),
                        version='1.0.0',
                        label=InputData(
                            'text'
                        ),
                        validation=RequiredConditionV1(
                            version='1.0.0'
                        )
                    )
                ],
                version='1.0.0',
            ),
            [
                ImageViewV1(
                    InputData(
                        'image_a',
                    ),
                    version='1.2.3',
                    full_height=True
                ),
                ImageViewV1(
                    InputData(
                        'image_b'
                    ),
                    version='1.2.3',
                    full_height=True
                )
            ],
            version='1.0.0'
        ),
        plugins=[
            HotkeysPluginV1(
                version='1.0.0',
                key_0=SetActionV1(
                    version='1.0.0',
                    data=RefComponent('vars.0'),
                    payload='failure'
                ),
                key_1=SetActionV1(
                    version='1.0.0',
                    data=RefComponent('vars.0'),
                    payload='a'
                ),
                key_2=SetActionV1(
                    version='1.0.0',
                    data=RefComponent('vars.0'),
                    payload='b'
                )
            )
        ],
        vars={'0': OutputData('result')}
    )

    result = ViewSpec.structure(view_spec_map)
    assert result.config == expected_result


def test_ref(view_spec_map):
    result = ViewSpec.structure(view_spec_map)
    assert result.config.plugins[0].key_0.data == RefComponent('vars.0')


def test_union_with_base_component_parsing(view_spec_map):
    result = ViewSpec.structure(view_spec_map)
    assert result.config.vars['0'] == OutputData('result')
    assert result.config.view.controls.items[1].label == InputData('text')


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


def test_get_input_and_output():
    tb_config = TemplateBuilder(
        view=SideBySideLayoutV1(
            version='1.0.0',
            controls=ListViewV1(
                version='1.0.0',
                items=[
                    RadioGroupFieldV1(
                        RefComponent(
                            'vars.0'
                        ),
                        version='1.0.0',
                        label='Какое фото вам больше нравится?',
                        options=[
                            GroupFieldOption(
                                'a',
                                'A',
                            ),
                            GroupFieldOption(
                                'b',
                                'B',
                                hint=TextareaFieldV1(
                                    InputData(
                                        'text'
                                    ),
                                    version='1.0.0'
                                )
                            ),
                            GroupFieldOption(
                                'failure',
                                'Картинки не загрузились'
                            )
                        ],
                    ),
                    TextareaFieldV1(
                        OutputData(
                            'why'
                        ),
                        version='1.0.0',
                        label=InputData(
                            'text'
                        ),
                        validation=RequiredConditionV1(
                            version='1.0.0'
                        )
                    )
                ]
            ),
            items=[
                ImageViewV1(
                    InputData('image_a'),
                    version='1.2.3',
                    full_height=True
                ),
                ImageViewV1(
                    InputData('image_b'),
                    version='1.2.3',
                    full_height=True
                )
            ]
        ),
        plugins=[
            HotkeysPluginV1(
                version='1.0.0',
                key_0=SetActionV1(
                    RefComponent('vars.0'),
                    'failure',
                    version='1.0.0'
                ),
                key_1=SetActionV1(
                    RefComponent('vars.0'),
                    'a',
                    version='1.0.0'
                ),
                key_2=SetActionV1(
                    RefComponent('vars.0'),
                    'b',
                    version='1.0.0'
                )
            )
        ],
        vars={'0': OutputData('result')}
    )

    expected_input = {
        'image_a': JsonSpec(),
        'image_b': JsonSpec(),
        'text': JsonSpec(),
    }

    expected_output = {
        'result': JsonSpec(),
        'why': JsonSpec
    }

    assert expected_input, expected_output == get_input_and_output(tb_config)
    assert expected_input, expected_output == get_input_and_output(tb_config.unstructure())
