import datetime
from operator import itemgetter
from typing import List
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client


@pytest.fixture
def task_suite_map():
    return {
        'pool_id': '21',
        'tasks': [
            {
                'input_values': {'image': 'http://images.com/1.png'}
            },
            {
                'input_values': {'image': 'http://images.com/2.png'},
                'known_solutions': [
                    {
                        'output_values': {'color': 'white'},
                        'correctness_weight': 1.0,
                    },
                    {
                        'output_values': {'color': 'gray'},
                        'correctness_weight': 0.71,
                    }
                ],
                'message_on_unknown_solution': 'Main color is white',
            }
        ],
        'overlap': 5,
        'infinite_overlap': False,
        'remaining_overlap': 5,
        'issuing_order_override': 10.3,
        'unavailable_for': ['tlk-user-i1d', 'tlk-user-i2d'],
        'reserved_for': ['tlk-user-i3d', 'tlk-user-i4d'],
        'traits_all_of': ['trait-1'],
        'traits_any_of': ['trait-2'],
        'traits_none_of_any': ['trait-3'],
        'longitude': 136.22,
        'latitude': 58.588,
    }


@pytest.fixture
def task_suite_map_with_readonly(task_suite_map):
    return {
        **task_suite_map,
        'id': 'task-suite-i1d',
        'mixed': False,
        'automerged': True,
        'created': '2015-12-13T23:57:12',
    }


def test_create_task_suite(requests_mock, toloka_client, toloka_url, task_suite_map, task_suite_map_with_readonly):

    def task_suites(request, context):
        assert task_suite_map == request.json()
        return task_suite_map_with_readonly

    requests_mock.post(f'{toloka_url}/task-suites', json=task_suites)

    # TODO: test creation parameters
    result = toloka_client.create_task_suite(client.unstructure(task_suite_map))
    assert task_suite_map_with_readonly == client.unstructure(result)


def test_create_task_suites(requests_mock, toloka_client, toloka_url):
    raw_request = [
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
        },
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': None}}],
        }
    ]

    raw_result = {
        'items': {
            '0': {
                'id': 'task-suite-i1d',
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
                'mixed': False,
                'created': '2016-07-09T14:39:00',
            }
        },
        'validation_errors': {
            '1': {
                'tasks.0.input_values.image': {
                    'code': 'VALUE_REQUIRED',
                    'message': 'May not be null'
                }
            }
        }
    }

    def task_suites(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.post(f'{toloka_url}/task-suites', json=task_suites, status_code=201)

    request = client.structure(raw_request, List[client.task_suite.TaskSuite])
    result = toloka_client.create_task_suites(request, async_mode=False, skip_invalid_items=True)
    assert raw_result == client.unstructure(result)


@pytest.fixture
def task_suites_map():
    return [
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
        },
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
        }
    ]


@pytest.fixture
def operation_running_map():
    return {
        'id': 'operation-i1d',
        'type': 'TASK_SUITE.BATCH_CREATE',
        'status': 'RUNNING',
        'submitted': '2015-12-13T23:32:01',
        'started': '2015-12-13T23:33:00',
        'parameters': {
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        'details': {'items_count': 2},
    }


@pytest.fixture
def operation_success_map(operation_running_map):
    return dict(operation_running_map, status='SUCCESS')


@pytest.fixture
def create_log():
    return [
        {
            'input': {
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
                 '__client_uuid': "e3e70682c2094cac629f6fbed82c07cd",
            },
            'output': {
                'task_suite_id': '00013b0abd--60094b06c680984b001e0071',
            },
            'success': True,
            'type': 'TASK_SUITE_CREATE',
        },
        {
            'input': {
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
                '__client_uuid': 'f728b4fa42485e3a0a5d2f346baa9455',
            },
            'output': {
                'task_suite_id': '00013b0abd--60094b06c680984b001e0072',
            },
            'success': True,
            'type': 'TASK_SUITE_CREATE',
        },
    ]


@pytest.fixture
def get_task_suites_map():
    return [
        {
            'id': '00013b0abd--60094b06c680984b001e0071',
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
            'mixed': False,
           'created': '2016-07-09T14:39:00',
        },
        {
            'id': '00013b0abd--60094b06c680984b001e0072',
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
            'mixed': False,
            'created': '2016-07-09T14:40:00',
        },
    ]


@pytest.fixture
def task_suites_result_map():
    return {
        'items': {
            '0': {
                'id': '00013b0abd--60094b06c680984b001e0071',
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
                'mixed': False,
                'created': '2016-07-09T14:39:00',
            },
            '1': {
                'id': '00013b0abd--60094b06c680984b001e0072',
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
                'mixed': False,
                'created': '2016-07-09T14:40:00',
            },
        },
    }


def test_create_task_suites_sync_through_async(
        requests_mock, toloka_client, toloka_url, no_uuid_random,
        task_suites_map, operation_running_map, operation_success_map,
        create_log, get_task_suites_map, task_suites_result_map
):

    def check_task_suites(request, context):
        assert {
            'operation_id': ['operation-i1d'],
            'skip_invalid_items': ['true'],
            'allow_defaults': ['true'],
            'open_pool': ['true'],
            'async_mode': ['true']
        } == parse_qs(urlparse(request.url).query)
        imcoming_task_suites = []
        for t in request.json():
            assert '__client_uuid' in t
            t.pop('__client_uuid')
            imcoming_task_suites.append(t)
        assert task_suites_map == imcoming_task_suites
        return operation_running_map

    # mocks
    requests_mock.post(f'{toloka_url}/task-suites', json=check_task_suites, status_code=201)
    requests_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}', json=operation_success_map, status_code=201)
    requests_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}/log', json=create_log, status_code=201)
    requests_mock.get(f'{toloka_url}/task-suites', json={'items': get_task_suites_map, 'has_more': False}, status_code=201)

    # Expanded syntax
    result = toloka_client.create_task_suites(
        [client.structure(t, client.task_suite.TaskSuite) for t in task_suites_map],
        operation_id='operation-i1d',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert task_suites_result_map == client.unstructure(result)


def test_create_task_suites_async(requests_mock, toloka_client, toloka_url):
    raw_request = [
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
        },
        {
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
        }
    ]

    raw_result = {
        'id': 'operation-i1d',
        'type': 'TASK_SUITE.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2015-12-13T23:32:01',
        'started': '2015-12-13T23:33:00',
        'parameters': {
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        'details': {'items_count': 2},
    }

    def task_suites(request, context):
        assert {
            'skip_invalid_items': ['true'],
            'allow_defaults': ['true'],
            'open_pool': ['true'],
            'async_mode': ['true']
        } == parse_qs(urlparse(request.url).query)
        assert raw_request == request.json()
        return raw_result

    requests_mock.post(f'{toloka_url}/task-suites', json=task_suites)

    request = client.structure(raw_request, List[client.task_suite.TaskSuite])

    # Request object syntax
    parameters = client.task_suite.TaskSuiteCreateRequestParameters(
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    result = toloka_client.create_task_suites_async(request, parameters)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_task_suites_async(
        request,
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert raw_result == client.unstructure(result)


def test_find_task_suites(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    raw_result = {'items': [task_suite_map_with_readonly], 'has_more': False}

    def task_suites(request, context):
        assert {
            'pool_id': ['21'],
            'created_lte': ['2020-02-01T00:00:00'],
            'overlap_gte': ['42'],
            'sort': ['-created'],
            'limit': ['100'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/task-suites', json=task_suites)

    # Request object syntax
    request = client.search_requests.TaskSuiteSearchRequest(
        pool_id=21,
        created_lte=datetime.datetime(2020, 2, 1),
        overlap_gte=42,
    )
    sort = client.search_requests.TaskSuiteSortItems(['-created'])
    result = toloka_client.find_task_suites(request, sort=sort, limit=100)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_task_suites(
        pool_id=21,
        created_lte=datetime.datetime(2020, 2, 1),
        overlap_gte=42,
        sort=['-created'],
        limit=100,
    )
    assert raw_result == client.unstructure(result)


def test_get_task_suites(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    task_suites = [dict(task_suite_map_with_readonly, id=f'task-suite-i{i}d') for i in range(50)]
    task_suites.sort(key=itemgetter('id'))

    def get_task_suites(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'pool_id': ['21'],
            'created_lte': ['2020-02-01T00:00:00'],
            'overlap_gte': ['42'],
            'sort': ['id'],
        } == params

        items = [task_suite for task_suite in task_suites if id_gt is None or task_suite['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != task_suites[-1]['id']}

    requests_mock.get(f'{toloka_url}/task-suites', json=get_task_suites)

    # Request object syntax
    request = client.search_requests.TaskSuiteSearchRequest(
        pool_id=21,
        created_lte=datetime.datetime(2020, 2, 1),
        overlap_gte=42,
    )
    result = toloka_client.get_task_suites(request)
    assert task_suites == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_task_suites(
        pool_id=21,
        created_lte=datetime.datetime(2020, 2, 1),
        overlap_gte=42,
    )
    assert task_suites == client.unstructure(list(result))


def test_get_task_suite(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):
    requests_mock.get(f'{toloka_url}/task-suites/task-suite-i1d', json=task_suite_map_with_readonly)
    result = toloka_client.get_task_suite('task-suite-i1d')
    assert task_suite_map_with_readonly == client.unstructure(result)


def test_patch_task_suite(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):
    raw_request = {'overlap': 12, 'infinite_overlap': False, 'issuing_order_override': 10.4}
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12, 'issuing_order_override': 10.4}

    def task_suites(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d', json=task_suites)

    # Request object syntax
    patch = client.structure(raw_request, client.task_suite.TaskSuitePatch)
    result = toloka_client.patch_task_suite('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)


def test_patch_task_suite_with_parameters(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12, 'infinite_overlap': False}

    def task_suites(request, context):
        params = parse_qs(urlparse(request.url).query)
        assert {'open_pool': ['true']} == params
        assert {'overlap': 12, 'infinite_overlap': False} == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d', json=task_suites)

    # Request object syntax
    patch = client.task_suite.TaskSuitePatch(overlap=12, open_pool=True)
    result = toloka_client.patch_task_suite('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_suite('task-suite-i1d', overlap=12, open_pool=True)
    assert raw_result == client.unstructure(result)


def test_patch_task_suite_overlap_or_min(requests_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    raw_patch = {'overlap': 10}
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12}

    def task_suites(request, context):
        assert raw_patch == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d/set-overlap-or-min', json=task_suites)

    # Request object syntax
    patch = client.structure(raw_patch, client.task_suite.TaskSuiteOverlapPatch)
    result = toloka_client.patch_task_suite_overlap_or_min('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_suite_overlap_or_min('task-suite-i1d', overlap=10)
    assert raw_result == client.unstructure(result)
