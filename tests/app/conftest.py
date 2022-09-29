import pytest
from decimal import Decimal


@pytest.fixture
def app_map():
    return {
        'constraints_description': 'constraints description',
        'default_item_price': Decimal(0.1),
        'description': 'app description',
        'examples': {},
        'id': '123',
        'image': 'image',
        'input_spec': {
            'id': {
                'type': 'string',
                'required': False,
                'hidden': False
            },
            'text': {
                'type': 'string',
                'required': True,
                'hidden': False
            }
        },
        'name': 'app name',
        'output_spec': {
            'result': {
                'type': 'array_string',
                'required': True,
                'hidden': False
            },
            'confidence': {
                'type': 'float',
                'required': False,
                'hidden': False
            }
        },
        'param_spec': {
            'fields': {
                'required': [
                    'default_language',
                    'name',
                    'instruction_text2_label',
                    'option_multiple_choice',
                    'option_other',
                    'instruction_classes',
                    'instruction_examples',
                    'instruction_intro'
                ],
                'properties': {
                    'name': {
                        'type': 'string'
                    },
                    'option_other': {
                        'type': 'boolean'
                    },
                    'default_language': {
                        'type': 'string'
                    },
                    'instruction_intro': {
                        'type': 'string'
                    },
                    'instruction_classes': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'required': [
                                'label',
                                'description',
                                'value'
                            ],
                            'properties': {
                                'label': {
                                    'type': 'string'
                                },
                                'value': {
                                    'type': 'string'
                                },
                                'description': {
                                    'type': 'string'
                                }
                            }
                        }
                    },
                    'instruction_examples': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'required': [
                                'description',
                                'label',
                                'text'
                            ],
                            'properties': {
                                'label': {
                                    'type': 'string'
                                },
                                'text': {
                                    'type': 'string'
                                },
                                'description': {
                                    'type': 'string'
                                }
                            }
                        }
                    },
                    'option_multiple_choice': {
                        'type': 'boolean'
                    },
                    'instruction_text_label': {
                        'type': 'string'
                    },
                }
            }
        },
        'input_format_info': {
            'examples': {
                'id': '1',
                'text': "Leslie Nielson is a very talented actor, who made a huge mistake by doing this film. It doesn't even come close to being funny. The best word to describe it is STUPID!",
            },
            'input_fields': [
                {'name': 'text', 'description': 'Text'},
                {'name': 'id', 'description': 'Optional identificator'},
            ],
            'format_description': 'Prepare TSV or JSON file with your data: single file for all tasks',
        }
    }


@pytest.fixture
def app_project_map():
    return {
        'app_id': '123',
        'parent_app_project_id': '',
        'name': 'ah-create-test',
        'parameters': {
            'name': 'ah-create-test'
        }
    }


@pytest.fixture
def app_project_map_with_readonly(app_project_map):
    return {
        **app_project_map,
        'id': '123',
        'status': 'READY',
        'created': '2021-09-29T15:13:38.491000',
        'errors': [],
        'item_price': 0.0000,
        'read_only': False,
        'app': {'id': '123', 'name': 'app_name'},
    }


@pytest.fixture
def app_item_map():
    return {
        'batch_id': '123',
        'input_data': {
            'id': '124',
            'text': 'I smell bad after the last night.'
        },
        'errors': [],
    }


@pytest.fixture
def app_item_map_with_readonly(app_item_map):
    return {
        **app_item_map,
        'id': '123',
        'app_project_id': '123',
        'status': 'COMPLETED',
        'output_data': {
            'result': 'correct',
            'confidence': Decimal(0.82)
        },
        'created_at': '2021-09-28T15:56:25.193000',
        'started_at': '2021-09-28T15:56:30.309920',
        'finished_at': '2021-09-28T16:07:12.307169',
        'errors': [],
    }


@pytest.fixture
def app_item_import_map():
    return {
        'id': '123',
        'records_count': 1000,
        'records_processed': 10,
        'errors': {}
    }


@pytest.fixture
def app_batch_map(app_item_import_map):
    return {
        'id': '123',
        'app_project_id': '123',
        'status': 'COMPLETED',
        'name': '1000-items',
        'items_count': 1000,
        'item_price': 0.0000,
        'cost': Decimal(0.0000),
        'cost_of_processed': Decimal(10.),
        'last_items_import': app_item_import_map,
        'confidence_avg': 50.,
        'items_processed_count': 10,
        'eta': '2021-09-28T16:07:13.400000',
        'items_per_state': {},
        'created_at': '2021-09-28T15:56:25.193000',
        'started_at': '2021-09-28T15:56:30.201000',
        'finished_at': '2021-09-28T16:07:13.400000',
        'read_only': False,
    }
