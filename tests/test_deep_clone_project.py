import copy

import httpx
import pytest
import toloka.client as client

from .testutils.util_functions import check_headers


@pytest.fixture
def original_project_map():
    return {
        'metadata': {
            'abc_service_id': ['4402'],
            'target_geo_region': ['WORLD']
        },
        'owner': {'id': 'cea0eec63247bcd0ee04339ea247ed4b', 'myself': True, 'company_id': '1000'},
        'public_name': 'My pretty project',
        'public_description': 'Perform my project please',
        'task_spec': {
            'input_spec': {
                'image': {
                    'required': True,
                    'hidden': False,
                    'type': 'url'
                },
            },
            'output_spec': {
                'answer': {
                    'required': True,
                    'hidden': False,
                    'allowed_values': ['true', 'false'],
                    'type': 'string'
                },
            },
            'view_spec': {
                'markup': '<dummy/>',
                'type': 'classic',
            },
        },
        'assignments_issuing_type': 'AUTOMATED',
        'assignments_automerge_enabled': False,
        'status': 'ACTIVE',
        'created': '2021-03-03T09:19:51.295000',
        'id': '404040',
        'public_instructions': 'Say Yes or No on your choise',
        'private_comment': '\0_0/'
    }


@pytest.fixture
def original_project_with_quality_map(original_project_map):
    new_project = copy.deepcopy(original_project_map)
    new_project['quality_control'] = {
        'training_requirement': {
            'training_pool_id': '20549529',
            'training_passing_skill_value': 70
        },
        'configs': [
            {
                'rules': [
                    {
                        'action': {
                            'parameters': {'scope': 'POOL', 'duration_unit': 'PERMANENT'},
                            'type': 'RESTRICTION_V2'
                        },
                        'conditions': [{'operator': 'GTE', 'value': 5, 'key': 'fast_submitted_count'}]
                    }
                ],
                'collector_config': {
                    'uuid': 'bc6135bb-4867-0ef6-9d31-d3bcbc7d1418',
                    'parameters': {'fast_submit_threshold_seconds': 45, 'history_size': 20},
                    'type': 'ASSIGNMENT_SUBMIT_TIME'
                },
            },
            {
                'rules': [
                    {
                        'action': {
                            'parameters': {'scope': 'PROJECT', 'duration_unit': 'PERMANENT', 'private_comment': 'wrong answers'},
                            'type': 'RESTRICTION_V2'
                        },
                        'conditions': [{'operator': 'LT', 'value': 60.0, 'key': 'correct_answers_rate'}]
                    },
                ],
                'collector_config': {
                    'uuid': '9c08bfc3-4685-dcf6-81d1-ebc464db2ffb',
                    'parameters': {'history_size': 10},
                    'type': 'GOLDEN_SET'
                },
            },
        ]
    }
    return new_project


@pytest.fixture
def original_pool_without_train_map():
    return {
        'project_id': '404040',
        'private_name': 'Pool without training',
        'may_contain_adult_content': False,
        'reward_per_assignment': 0.02,
        'assignment_max_duration_seconds': 600,
        'defaults': {'default_overlap_for_new_task_suites': 5},
        'will_expire': '2022-01-17T21:45:00.034000',
        'auto_close_after_complete_delay_seconds': 0,
        'auto_accept_solutions': True,
        'auto_accept_period_day': 21,
        'assignments_issuing_config': {'issue_task_suites_in_creation_order': False},
        'priority': 0,
        'filter': {'and': [{'or': [{'operator': 'IN', 'value': 'EN', 'key': 'languages', 'category': 'profile'}]}]},
        'quality_control': {
            'configs': [
                {
                    'rules': [
                        {
                            'action': {
                                'parameters': {'scope': 'POOL', 'duration_unit': 'PERMANENT'},
                                'type': 'RESTRICTION_V2'
                            },
                            'conditions': [{'operator': 'GTE', 'value': 5, 'key': 'fast_submitted_count'}]
                        },
                    ],
                    'collector_config': {
                        'uuid': 'bc6135bb-0ef6-4867-9d31-bc7d1418d3bc',
                        'parameters': {'fast_submit_threshold_seconds': 45, 'history_size': 20},
                        'type': 'ASSIGNMENT_SUBMIT_TIME'
                    },
                },
                {
                    'rules': [
                        {
                            'action': {
                                'parameters': {'scope': 'PROJECT', 'duration_unit': 'PERMANENT', 'private_comment': 'wrong answers'},
                                'type': 'RESTRICTION_V2'
                            },
                            'conditions': [{'operator': 'LT', 'value': 60.0, 'key': 'correct_answers_rate'}]
                        },
                    ],
                    'collector_config': {
                        'uuid': '9c08bfc3-dcf6-4685-81d1-64db2ffbebc4',
                        'parameters': {'history_size': 10},
                        'type': 'GOLDEN_SET'
                    },
                },
            ]
        },
        'mixer_config': {
            'real_tasks_count': 9,
            'golden_tasks_count': 1,
            'training_tasks_count': 0,
            'min_real_tasks_count': 9,
            'min_golden_tasks_count': 0,
            'force_last_assignment': True
        },
        'owner': {'id': 'cea0eec63247bcd0ee04339ea247ed4b', 'myself': True, 'company_id': '1000'},
        'id': '21946541',
        'status': 'CLOSED',
        'created': '2021-03-03T09:19:54.810000',
        'type': 'REGULAR'
    }


@pytest.fixture
def original_pool_with_train_map():
    return {
        'project_id': '404040',
        'private_name': 'Pool with training',
        'may_contain_adult_content': False,
        'reward_per_assignment': 0.02,
        'assignment_max_duration_seconds': 600,
        'defaults': {'default_overlap_for_new_task_suites': 5},
        'will_expire': '2022-01-17T21:45:00.034000',
        'auto_close_after_complete_delay_seconds': 0,
        'auto_accept_solutions': True,
        'auto_accept_period_day': 21,
        'assignments_issuing_config': {'issue_task_suites_in_creation_order': False},
        'priority': 0,
        'filter': {
            'and': [
                {'or': [{'operator': 'IN', 'value': 'EN', 'key': 'languages', 'category': 'profile'}]},
                {'or': [{'key': '100', 'operator': 'EQ', 'value': None, 'category': 'skill'}]},
                {'or': [{'key': '101', 'operator': 'EQ', 'value': None, 'category': 'skill'}]},
                {'or': [{'key': '102', 'operator': 'EQ', 'value': None, 'category': 'skill'}]},
                {'or': [{'key': '102', 'operator': 'EQ', 'value': None, 'category': 'skill'}]}
            ]
        },
        'quality_control': {
            'training_requirement': {
                'training_pool_id': '20549529',
                'training_passing_skill_value': 70
            },
            'configs': [
                {
                    'rules': [
                        {
                            'action': {
                                'parameters': {'scope': 'PROJECT', 'duration_unit': 'PERMANENT'},
                                'type': 'RESTRICTION_V2'
                            },
                            'conditions': [{'operator': 'GTE', 'value': 10.0, 'key': 'income_sum_for_last_24_hours'}]
                        },
                    ],
                    'collector_config': {
                        'uuid': 'e3aaf57f-f229-4435-84e7-44291d9b0937',
                        'type': 'INCOME'
                    },
                },
                {
                    'rules': [
                        {
                            'action': {
                                'parameters': {'scope': 'POOL', 'duration_unit': 'PERMANENT'},
                                'type': 'RESTRICTION_V2'
                            },
                            'conditions': [{'operator': 'GTE', 'value': 10, 'key': 'skipped_in_row_count'}]
                        },
                    ],
                    'collector_config': {
                        'uuid': '4f4d1260-c8a0-409a-82ba-42ed1338f149',
                        'type': 'SKIPPED_IN_ROW_ASSIGNMENTS'
                    },
                },
            ]
        },
        'mixer_config': {
            'real_tasks_count': 9,
            'golden_tasks_count': 1,
            'training_tasks_count': 0,
            'min_real_tasks_count': 9,
            'min_golden_tasks_count': 0,
            'force_last_assignment': True
        },
        'owner': {'id': 'cea0eec63247bcd0ee04339ea247ed4b', 'myself': True, 'company_id': '1000'},
        'id': '21946544',
        'status': 'CLOSED',
        'created': '2021-03-03T09:19:55.375000',
        'type': 'REGULAR'
    }


@pytest.fixture
def original_train_map():
    return {
        'project_id': '404040',
        'private_name': 'This is Training',
        'may_contain_adult_content': False,
        'assignment_max_duration_seconds': 600,
        'mix_tasks_in_creation_order': False,
        'shuffle_tasks_in_task_suite': True,
        'training_tasks_in_task_suite_count': 7,
        'task_suites_required_to_pass': 3,
        'inherited_instructions': True,
        'public_instructions': '',
        'owner': {'id': 'cea0eec63247bcd0ee04339ea247ed4b', 'myself': True, 'company_id': '1000'},
        'id': '20549529',
        'status': 'CLOSED',
        'last_close_reason': 'MANUAL',
        'created': '2021-01-17T22:35:24.270000',
        'last_started': '2021-01-18T11:12:53.630000',
        'last_stopped': '2021-01-18T15:02:00.843000'
    }


@pytest.fixture
def new_project_id():
    return '505050'


@pytest.fixture
def new_training_id():
    return '200300500'


@pytest.fixture
def clone_project_map(original_project_map, new_project_id):
    new_project = copy.deepcopy(original_project_map)
    new_project['id'] = new_project_id
    return new_project


@pytest.fixture
def clone_project_with_quality_map(original_project_with_quality_map, new_project_id):
    new_project = copy.deepcopy(original_project_with_quality_map)
    new_project['id'] = new_project_id
    return new_project


@pytest.fixture
def clone_train_map(original_train_map, new_project_id, new_training_id):
    new_train = copy.deepcopy(original_train_map)
    new_train['id'] = new_training_id
    new_train['project_id'] = new_project_id
    return new_train


@pytest.fixture
def clone_pool_without_train_map(original_pool_without_train_map, new_project_id):
    new_pool = copy.deepcopy(original_pool_without_train_map)
    new_pool['id'] = '1111'
    new_pool['project_id'] = new_project_id
    return new_pool


@pytest.fixture
def clone_pool_with_train_map(original_pool_with_train_map, new_project_id, new_training_id):
    new_pool = copy.deepcopy(original_pool_with_train_map)
    new_pool['id'] = '2222'
    new_pool['project_id'] = new_project_id
    new_pool['quality_control']['training_requirement']['training_pool_id'] = new_training_id
    return new_pool


def test_clone_project(
    respx_mock, toloka_client, toloka_url, original_project_with_quality_map, clone_project_map,
    clone_project_with_quality_map, original_train_map, clone_train_map, original_pool_without_train_map,
    clone_pool_without_train_map, original_pool_with_train_map, clone_pool_with_train_map
):

    def original_project_with_quality(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'get_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=original_project_with_quality_map, status_code=200)

    def clone_project(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'create_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=clone_project_map, status_code=201)

    def clone_project_with_quality(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'update_project',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=clone_project_with_quality_map, status_code=200)

    respx_mock.get(f'{toloka_url}/projects/404040').mock(side_effect=original_project_with_quality)
    respx_mock.post(f'{toloka_url}/projects').mock(side_effect=clone_project)
    respx_mock.put(f'{toloka_url}/projects/505050').mock(side_effect=clone_project_with_quality)

    def get_trainings(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'find_trainings',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json={'items': [original_train_map], 'has_more': False}, status_code=200)

    def clone_train(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'create_training',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=clone_train_map, status_code=201)

    respx_mock.get(f'{toloka_url}/trainings').mock(side_effect=get_trainings)
    respx_mock.post(f'{toloka_url}/trainings').mock(side_effect=clone_train)

    def original_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'find_pools',
        }
        check_headers(request, expected_headers)

        return httpx.Response(
            json={'items': [original_pool_without_train_map, original_pool_with_train_map], 'has_more': False},
            status_code=200
        )

    respx_mock.get(f'{toloka_url}/pools').mock(side_effect=original_pool)

    created_pools = [clone_pool_without_train_map, clone_pool_with_train_map]

    def create_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'clone_project',
            'X-Low-Level-Method': 'create_pool',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=created_pools.pop(0), status_code=201)

    respx_mock.post(f'{toloka_url}/pools').mock(side_effect=create_pool)

    new_project, new_pools, new_trainings = toloka_client.clone_project('404040')

    assert clone_project_map == client.unstructure(clone_project_map)
    assert clone_pool_without_train_map == client.unstructure(new_pools[0])
    assert clone_pool_with_train_map == client.unstructure(new_pools[1])
    assert clone_train_map == client.unstructure(new_trainings[0])
