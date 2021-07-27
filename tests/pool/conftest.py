import pytest


@pytest.fixture
def pool_map():
    return {
        'type': 'REGULAR',
        'project_id': '10',
        'private_name': 'pool_v12_231',
        'public_description': '42',
        'may_contain_adult_content': True,
        'will_expire': '2016-03-23T12:59:00',
        'auto_close_after_complete_delay_seconds': 600,
        'reward_per_assignment': 0.03,
        'dynamic_pricing_config': {
            'type': 'SKILL',
            'skill_id': '123123',
            'intervals': [
                {'from': 50, 'to': 79, 'reward_per_assignment': 0.05},
                {'from': 80, 'reward_per_assignment': 0.1},
            ]
        },
        'dynamic_overlap_config': {
            'type': 'BASIC',
            'max_overlap': 5,
            'min_confidence': 0.95,
            'answer_weight_skill_id': '42',
            'fields': [{'name': 'out1'}],
        },
        'metadata': {'testKey': ['testValue']},
        'assignment_max_duration_seconds': 600,
        'auto_accept_solutions': True,
        'priority': 10,
        'defaults': {
            'default_overlap_for_new_task_suites': 3,
            'default_overlap_for_new_tasks': 2,
        },
        'mixer_config': {
            'real_tasks_count': 10,
            'golden_tasks_count': 2,
            'training_tasks_count': 1,
            'min_training_tasks_count': 0,
            'min_golden_tasks_count': 1,
            'force_last_assignment': False,
            'force_last_assignment_delay_seconds': 10,
            'mix_tasks_in_creation_order': False,
            'shuffle_tasks_in_task_suite': True,
            'golden_task_distribution_function': {
                'scope': 'POOL',
                'distribution': 'UNIFORM',
                'window_days': 5,
                'intervals': [
                    {'to': 50, 'frequency': 5},
                    {'from': 100, 'frequency': 50},
                ],
            }
        },
        'assignments_issuing_config': {
            'issue_task_suites_in_creation_order': True,
        },
        'filter': {
            'and': [
                {
                    'category': 'profile',
                    'key': 'adult_allowed',
                    'operator': 'EQ',
                    'value': True,
                },
                {
                    'or': [
                        {
                            'category': 'skill',
                            'key': '20',
                            'operator': 'GTE',
                            'value': 60
                        },
                        {
                            'category': 'skill',
                            'key': '22',
                            'operator': 'GT',
                            'value': 95,
                        }
                    ]
                },
            ]
        },
        'quality_control': {
            'captcha_frequency': 'LOW',
            'checkpoints_config': {
                'real_settings': {
                    'target_overlap': 5,
                    'task_distribution_function': {
                        'scope': 'PROJECT',
                        'distribution': 'UNIFORM',
                        'window_days': 7,
                        'intervals': [
                            {'to': 100, 'frequency': 5},
                            {'from': 101, 'frequency': 50},
                        ],
                    },
                },
            },
            'configs': [
                {
                    'collector_config': {
                        'type': 'CAPTCHA',
                        'parameters': {'history_size': 5},
                    },
                    'rules': [
                        {
                            'conditions': [
                                {
                                    'key': 'stored_results_count',
                                    'operator': 'EQ',
                                    'value': 5
                                },
                                {
                                    'key': 'success_rate',
                                    'operator': 'LTE',
                                    'value': 60.0,
                                }
                            ],
                            'action': {
                                'type': 'RESTRICTION',
                                'parameters': {
                                    'scope': 'POOL',
                                    'duration_days': 10,
                                    'private_comment': 'ban in pool',
                                }
                            }
                        }
                    ]
                }
            ]
        }
    }


@pytest.fixture
def pool_map_with_readonly(pool_map):
    return {
        **pool_map,
        'id': '21',
        'owner': {'id': 'requester-1', 'myself': True, 'company_id': '1'},
        'type': 'REGULAR',
        'created': '2015-12-16T12:55:01',
        'last_started': '2015-12-17T08:00:01',
        'last_stopped': '2015-12-18T08:00:01',
        'last_close_reason': 'MANUAL',
        'status': 'CLOSED',
    }


@pytest.fixture
def open_pool_map_with_readonly(pool_map_with_readonly):
    return {
        **pool_map_with_readonly,
        'status': 'OPEN',
    }


@pytest.fixture
def training_pool_map():
    return {
        'id': '22',
        'owner': {
            'id': 'requester-1',
            'myself': True,
            'company_id': '1'
        },
        'type': 'TRAINING',
        'project_id': '10',
        'private_name': 'training_v12_231',
        'public_description': '42',
        'public_instructions': 'training instructions',
        'may_contain_adult_content': True,
        'reward_per_assignment': 0.00,
        'assignment_max_duration_seconds': 600,
        'auto_accept_solutions': True,
        'priority': 0,
        'defaults': {
            'default_overlap_for_new_task_suites': 30_000,
        },
        'mixer_config': {
            'real_tasks_count': 0,
            'golden_tasks_count': 0,
            'training_tasks_count': 7,
            'min_training_tasks_count': 1,
            'force_last_assignment': False,
            'force_last_assignment_delay_seconds': 10,
            'mix_tasks_in_creation_order': False,
            'shuffle_tasks_in_task_suite': True,
        },
        'assignments_issuing_config': {
            'issue_task_suites_in_creation_order': True,
        },
        'quality_control': {
            'configs': [
                {
                    'collector_config': {
                        'type': 'TRAINING',
                        'uuid': 'cdf0f2ee-04e4-11e8-8a8d-6c96cfdb64bb'
                    },
                    'rules': [
                        {
                            'conditions': [
                                {
                                    'key': 'submitted_assignments_count',
                                    'operator': 'EQ',
                                    'value': 5
                                }
                            ],
                            'action': {
                                'type': 'SET_SKILL_FROM_OUTPUT_FIELD',
                                'parameters': {
                                    'skill_id': '676',
                                    'from_field': 'correct_answers_rate',
                                }
                            }
                        },
                        {
                            'conditions': [
                                {
                                    'key': 'next_assignment_available',
                                    'operator': 'EQ',
                                    'value': False
                                },
                                {
                                    'key': 'total_answers_count',
                                    'operator': 'GT',
                                    'value': 0,
                                }
                            ],
                            'action': {
                                'type': 'SET_SKILL_FROM_OUTPUT_FIELD',
                                'parameters': {
                                    'skill_id': '676',
                                    'from_field': 'correct_answers_rate',
                                }
                            }
                        }
                    ]
                }
            ]
        },
        'training_config': {
            'training_skill_ttl_days': 5,
        },
        'status': 'OPEN',
        'created': '2017-12-03T12:03:00',
        'last_started': '2017-12-04T12:12:03',
    }
