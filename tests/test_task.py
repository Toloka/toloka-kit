import datetime
from operator import itemgetter
from urllib.parse import urlparse, parse_qs
from uuid import uuid4

import pytest
import toloka.client as client


@pytest.fixture
def task_map():
    return {
        'pool_id': '21',
        'input_values': {'image': 'http://images.com/1.png'},
        'known_solutions': [
            {
                'output_values': {'color': 'white'},
                'correctness_weight': 1.0,
            },
            {
                'output_values': {'color': 'gray'},
                'correctness_weight': 0.71,
            },
        ],
        'message_on_unknown_solution': 'Main color is white',
        'baseline_solutions': [
            {
                'output_values': {'color': 'white'},
                'confidence_weight': 1.0,
            },
            {
                'output_values': {'color': 'gray'},
                'confidence_weight': 0.71,
            },
        ],
        'overlap': 3,
        'infinite_overlap': False,
        'remaining_overlap': 3,
        'unavailable_for': ['user-1id'],
        'reserved_for': ['user-2id'],
        'traits_all_of': ['trait-1'],
        'traits_any_of': ['trait-2'],
        'traits_none_of_any': ['trait-3'],
    }


@pytest.fixture
def task_map_with_readonly(task_map):
    return {**task_map, 'created': '2016-10-09T11:42:01'}


def test_create_task(requests_mock, toloka_client, toloka_url, task_map, task_map_with_readonly):

    def tasks(request, context):
        assert task_map == request.json()
        return task_map_with_readonly

    requests_mock.post(f'{toloka_url}/tasks', json=tasks, status_code=201)
    result = toloka_client.create_task(client.structure(task_map, client.task.Task))
    assert task_map_with_readonly == client.unstructure(result)


def test_create_tasks(requests_mock, toloka_client, toloka_url, task_map, task_map_with_readonly):
    tasks_map = [task_map, {'pool_id': '21', 'input_values': {'image': None}}]
    raw_result = {
        'items': {'0': task_map_with_readonly},
        'validation_errors': {
            '1': {'input_values.image': {'code': 'VALUE_REQUIRED', 'message': 'May not be null'}},
        }
    }

    def tasks(request, context):
        assert {'allow_defaults': ['true']} == parse_qs(urlparse(request.url).query)
        assert tasks_map == request.json()
        return raw_result

    requests_mock.post(f'{toloka_url}/tasks', json=tasks, status_code=201)

    # raise ValueError(client.unstructure(client.task.CreateTasksParameters(allow_defaults=True)))

    # Request object syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        client.task.CreateTasksParameters(allow_defaults=True)
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        allow_defaults=True
    )
    assert raw_result == client.unstructure(result)


def test_create_tasks_async(requests_mock, toloka_client, toloka_url):
    tasks_map = [
        {'pool_id': '21', 'input_values': {'image': 'http://images.com/1.png'}},
        {'pool_id': '21', 'input_values': {'image': 'http://images.com/2.png'}},
    ]

    operation_map = {
        'id': '281073ea-ab34-416e-a028-47421ff1b166',
        'type': 'TASK.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2016-10-10T20:33:01',
        'started': '2016-10-10T23:33:00',
        'parameters': {'skip_invalid_items': True, 'allow_defaults': True, 'open_pool': True},
        'details': {'items_count': 2},
    }

    def tasks(request, context):
        assert {
            'operation_id': ['281073ea-ab34-416e-a028-47421ff1b166'],
            'skip_invalid_items': ['true'],
            'allow_defaults': ['true'],
            'open_pool': ['true'],
            'async_mode': ['true'],
        } == parse_qs(urlparse(request.url).query)
        assert tasks_map == request.json()
        return operation_map

    requests_mock.post(f'{toloka_url}/tasks', json=tasks, status_code=201)

    # Request object syntax
    result = toloka_client.create_tasks_async(
        [client.structure(task, client.task.Task) for task in tasks_map],
        client.task.CreateTasksAsyncParameters(
            operation_id='281073ea-ab34-416e-a028-47421ff1b166',
            skip_invalid_items=True,
            allow_defaults=True,
            open_pool=True,
        )
    )
    assert operation_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_tasks_async(
        [client.structure(task, client.task.Task) for task in tasks_map],
        operation_id='281073ea-ab34-416e-a028-47421ff1b166',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert operation_map == client.unstructure(result)


def test_find_tasks(requests_mock, toloka_client, toloka_url, task_map_with_readonly):

    raw_result = {'items': [task_map_with_readonly], 'has_more': False}

    def tasks(request, context):
        assert {
            'pool_id': ['21'],
            'created_gt': ['2001-01-01T12:00:00'],
            'overlap_gte': ['42'],
            'sort': ['id,-created'],
            'limit': ['20']
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/tasks', json=tasks)

    # Request object syntax
    request = client.search_requests.TaskSearchRequest(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0),
        overlap_gte=42,
    )
    sort = client.search_requests.TaskSortItems(['id', '-created'])
    result = toloka_client.find_tasks(request, sort=sort, limit=20)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_tasks(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0),
        overlap_gte=42,
        sort=['id', '-created'],
        limit=20,
    )
    assert raw_result == client.unstructure(result)


def test_get_tasks(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    tasks = [dict(task_map_with_readonly, id=str(uuid4())) for _ in range(50)]
    tasks.sort(key=itemgetter('id'))

    def get_tasks(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'pool_id': ['21'],
            'created_gt': ['2001-01-01T12:00:00'],
            'overlap_gte': ['42'],
            'sort': ['id'],
        } == params

        items = [task for task in tasks if id_gt is None or task['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != tasks[-1]['id']}

    requests_mock.get(f'{toloka_url}/tasks', json=get_tasks)

    # Request object syntax
    request = client.search_requests.TaskSearchRequest(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0),
        overlap_gte=42,
    )
    result = toloka_client.get_tasks(request)
    assert tasks == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_tasks(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0),
        overlap_gte=42,
    )
    assert tasks == client.unstructure(list(result))


def test_get_task(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    requests_mock.get(f'{toloka_url}/tasks/task-1', json=task_map_with_readonly)
    result = toloka_client.get_task('task-1')
    assert task_map_with_readonly == client.unstructure(result)


def test_patch_task(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'overlap': 10}
    raw_result = {**task_map_with_readonly, **raw_request}

    def tasks(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/tasks/task-1', json=tasks)

    # Request object syntax
    request = client.unstructure(raw_request)
    result = toloka_client.patch_task('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task('task-1', overlap=10)
    assert raw_result == client.unstructure(result)


def test_patch_task_with_baseline_solution(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {
        'baseline_solutions': [{
            'output_values': {'color': 'green'},
            'confidence_weight': 4.2,
        }]
    }
    raw_result = {**task_map_with_readonly, **raw_request}

    def tasks(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/tasks/task-1', json=tasks)

    # Request object syntax
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task(
        'task-1',
        baseline_solutions=[
            client.task.Task.BaselineSolution(
                output_values={'color': 'green'},
                confidence_weight=4.2,
            )
        ]
    )
    assert raw_result == client.unstructure(result)


def test_task_overlap_or_min(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'overlap': 10}
    raw_result = {**task_map_with_readonly, 'overlap': 12}

    def tasks(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/tasks/task-1/set-overlap-or-min', json=tasks)

    # Request object syntax
    request = client.unstructure(raw_request)
    result = toloka_client.patch_task_overlap_or_min('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_overlap_or_min('task-1', overlap=10)
    assert raw_result == client.unstructure(result)


def test_task_overlap_or_min_infinite_overlap(requests_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'infinite_overlap': True}
    raw_result = task_map_with_readonly

    def tasks(request, context):
        assert raw_request == request.json()
        return raw_result

    requests_mock.patch(f'{toloka_url}/tasks/task-1/set-overlap-or-min', json=tasks)

    # Request object syntax
    request = client.unstructure(raw_request)
    result = toloka_client.patch_task_overlap_or_min('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_overlap_or_min('task-1', infinite_overlap=True)
    assert raw_result == client.unstructure(result)
