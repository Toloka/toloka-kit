"""Tests for Real-life bugs"""
from toloka.client.project.template_builder import TemplateBuilder
from toloka.client.project.template_builder.data import InputData, OutputData
from toloka.client.project.template_builder.fields import GroupFieldOption, TextareaFieldV1, RadioGroupFieldV1
from toloka.client.project.template_builder.layouts import SideBySideLayoutV1
from toloka.client.project.template_builder.plugins import TolokaPluginV1
from toloka.client.project.template_builder.view import CollapseViewV1, GroupViewV1, ListViewV1, TextViewV1


def test_tolokakit_467():
    """Issue TOLOKAKIT-467"""

    raw_tb = {
        'plugins': [
            {
                'type': 'plugin.toloka',
                'layout': {'kind': 'scroll', 'taskWidth': 1200},
                'notifications': [
                    {'type': 'view.text', 'content': 'notification1'},
                    {'type': 'view.text', 'content': 'notification2'},
                ]
            }
        ],
        'view': {
            'type': 'layout.side-by-side',
            'items': [
                {
                    'type': 'view.group',
                    'content': {
                        'type': 'view.text',
                        'content': {'type': 'data.input', 'path': 'text_a'}
                    }
                },
                {
                    'type': 'view.group',
                    'content': {
                        'type': 'view.text',
                        'content': {'type': 'data.input', 'path': 'text_b'}
                    }
                }
            ],
            'controls': {
                'type': 'view.list',
                'items': [
                    {
                        'type': 'field.radio-group',
                        'label': 'Which one is better?',
                        'data': {'type': 'data.output', 'path': 'choice'},
                        'options': [
                            {'label': 'A', 'value': 'a'},
                            {'label': 'B', 'value': 'b'},
                        ],
                    },
                    {
                        'type': 'view.collapse',
                        'label': 'Comment (optional)',
                        'content': {
                            'type': 'field.textarea',
                            'data': {'type': 'data.output', 'path': 'comment'}
                        }
                    }
                ]
            }
        }
    }

    tb = TemplateBuilder(
        plugins=[
            TolokaPluginV1(
                layout=TolokaPluginV1.TolokaPluginLayout(
                    kind=TolokaPluginV1.TolokaPluginLayout.Kind.SCROLL,
                    task_width=1200.0,
                ),
                notifications=[
                    TextViewV1('notification1'),
                    TextViewV1('notification2'),
                ],
            )
        ],
        view=SideBySideLayoutV1(
            items=[
                GroupViewV1(TextViewV1(InputData('text_a'))),
                GroupViewV1(TextViewV1(InputData('text_b'))),
            ],
            controls=ListViewV1([
                RadioGroupFieldV1(
                    data=OutputData('choice'),
                    label='Which one is better?',
                    options=[
                        GroupFieldOption(value='a', label='A'),
                        GroupFieldOption(value='b', label='B'),
                    ],
                ),
                CollapseViewV1(
                    label='Comment (optional)',
                    content=TextareaFieldV1(OutputData('comment')),
                ),
            ]),
        ),
    )

    assert tb == TemplateBuilder.structure(raw_tb)
