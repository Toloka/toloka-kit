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


def test_create_tasks_with_error(requests_mock, toloka_client, toloka_url, task_map, task_map_with_readonly):
    tasks_map = [task_map, {'pool_id': '21', 'input_values': {'image': None}}]
    raw_result = {
        'items': {'0': task_map_with_readonly},
        'validation_errors': {
            '1': {'input_values.image': {'code': 'VALUE_REQUIRED', 'message': 'May not be null'}},
        }
    }

    def tasks(request, context):
        assert {'allow_defaults': ['true'], 'async_mode': ['false']} == parse_qs(urlparse(request.url).query)
        assert tasks_map == request.json()
        return raw_result

    requests_mock.post(f'{toloka_url}/tasks', json=tasks, status_code=201)

    # raise ValueError(client.unstructure(client.task.CreateTasksParameters(allow_defaults=True)))

    # Request object syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        client.task.CreateTasksParameters(allow_defaults=True, async_mode=False)
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        allow_defaults=True,
        async_mode=False,
    )
    assert raw_result == client.unstructure(result)


@pytest.fixture
def tasks_map():
    return [
        {'pool_id': '21', 'input_values': {'image': 'http://images.com/1.png'}},
        {'pool_id': '22', 'input_values': {'image': 'http://images.com/2.png'}},
        {'pool_id': '22', 'input_values': {'imagis': 'http://images.com/3.png'}}
    ]


@pytest.fixture
def operation_running_map():
    return {
        'id': '281073ea-ab34-416e-a028-47421ff1b166',
        'type': 'TASK.BATCH_CREATE',
        'status': 'RUNNING',
        'submitted': '2016-10-10T20:33:01',
        'started': '2016-10-10T23:33:00',
        'parameters': {'skip_invalid_items': True, 'allow_defaults': True, 'open_pool': True},
        'details': {'items_count': 2},
    }


@pytest.fixture
def operation_success_map(operation_running_map):
    return dict(operation_running_map, status='SUCCESS')


@pytest.fixture
def create_tasks_log():
    return [
        {
            'input': {
                'input_values': {
                    'image': 'http://images.com/1.png'
                },
                'pool_id': '21',
                '__client_uuid': 'e3e70682c2094cac629f6fbed82c07cd',
            },
            'output': {
                'task_id': '00014495f0--60213f7c25a8b84e2ffb7a2c'
            },
            'success': True,
            'type': 'TASK_CREATE'
        },
        {
            'input': {
                'input_values': {
                    'image': 'http://images.com/2.png'
                },
                'pool_id': '22',
                '__client_uuid': 'f728b4fa42485e3a0a5d2f346baa9455',
            },
            'output': {
                'task_id': '00014495f0--60213f7c25a8b84e2ffb7a3b'
            },
            'success': True,
            'type': 'TASK_CREATE'
        },
        {
            'input': {
                'input_values': {
                    'image': 'http://images.com/2.png'
                },
                'pool_id': '22',
                '__client_uuid': 'eb1167b367a9c3787c65c1e582e2e662',
            },
            'output': {
                'input_values.image': {
                    'code': 'VALUE_REQUIRED',
                    'message': 'Value must be present and not equal to null'
                },
                'input_values.imagis': {
                    'code': 'VALUE_NOT_ALLOWED',
                    'message': 'Unknown field name'
                }
            },
            'success': False,
            'type': 'TASK_VALIDATE'
        },
        {
            'input': {
                'pool_id': 22
            },
            'output': {
                'code': 'EMPTY_POOL',
                'message': 'Pool contains no tasks. Operation is not allowed',
                'request_id': 'ao_c8e4cb72-8d4b-4894-bc6e-65a403e6337e',
            },
            'success': False,
            'type': 'POOL_OPEN',
        },
    ]


@pytest.fixture
def created_tasks_21_map():
    return [
        {
            'id': '00014495f0--60213f7c25a8b84e2ffb7a2c',
            'pool_id': '21',
            'input_values': {'image': 'http://images.com/1.png'},
            'overlap': 1,
            'infinite_overlap': False,
            'remaining_overlap': 1,
        }
    ]


@pytest.fixture
def created_tasks_22_map():
    return [
        {
            'id': '00014495f0--60213f7c25a8b84e2ffb7a3b',
            'pool_id': '22',
            'input_values': {'image': 'http://images.com/2.png'},
            'overlap': 1,
            'infinite_overlap': False,
            'remaining_overlap': 1,
        }
    ]


@pytest.fixture
def task_create_result_map():
    return {
        'items': {
            '0': {
                'input_values': {'image': 'http://images.com/1.png'},
                'id': '00014495f0--60213f7c25a8b84e2ffb7a2c',
                'infinite_overlap': False,
                'overlap': 1,
                'pool_id': '21',
                'remaining_overlap': 1
            },
            '1': {
                'input_values': {'image': 'http://images.com/2.png'},
                'id': '00014495f0--60213f7c25a8b84e2ffb7a3b',
                'infinite_overlap': False,
                'overlap': 1,
                'pool_id': '22',
                'remaining_overlap': 1
            },
        },
        'validation_errors':
        {
            '2': {
                'input_values.image': {
                    'code': 'VALUE_REQUIRED',
                    'message': 'Value must be present and not equal to null'
                },
                'input_values.imagis': {
                    'code': 'VALUE_NOT_ALLOWED',
                    'message': 'Unknown field name'
                },
            },
        }
    }


def test_create_tasks_sync_through_async(
        requests_mock, toloka_client, toloka_url, no_uuid_random,
        tasks_map, operation_running_map, operation_success_map,
        create_tasks_log, created_tasks_21_map, created_tasks_22_map,
        task_create_result_map
):

    def check_tasks(request, context):
        assert {
            'operation_id': ['281073ea-ab34-416e-a028-47421ff1b166'],
            'skip_invalid_items': ['true'],
            'allow_defaults': ['true'],
            'open_pool': ['true'],
            'async_mode': ['true'],
        } == parse_qs(urlparse(request.url).query)
        imcoming_tasks = []
        for t in request.json():
            assert '__client_uuid' in t
            t.pop('__client_uuid')
            imcoming_tasks.append(t)
        assert tasks_map == imcoming_tasks
        return operation_running_map

    def return_tasks_by_pool(request, context):
        params = parse_qs(urlparse(request.url).query)
        res_map = created_tasks_21_map if params['pool_id'][0] == '21' else created_tasks_22_map
        return {'items': res_map, 'has_more': False}

    # mocks
    # create_task -> operation
    requests_mock.post(f'{toloka_url}/tasks', json=check_tasks, status_code=201)
    # wait_operation -> operation Success
    requests_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}', json=operation_success_map, status_code=201)
    # get_log -> log_res
    requests_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}/log', json=create_tasks_log, status_code=201)
    # get tasks from pools (2 calls - for each pool)
    requests_mock.get(f'{toloka_url}/tasks', json=return_tasks_by_pool, status_code=201)

    # Expanded syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        operation_id='281073ea-ab34-416e-a028-47421ff1b166',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert task_create_result_map == client.unstructure(result)


def test_create_tasks_sync(requests_mock, toloka_client, toloka_url, tasks_map, task_create_result_map):
    requests_mock.post(f'{toloka_url}/tasks', json=task_create_result_map, status_code=201)

    # Expanded syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        operation_id='281073ea-ab34-416e-a028-47421ff1b166',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
        async_mode=False,
    )
    assert task_create_result_map == client.unstructure(result)


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
        client.task.CreateTasksParameters(
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
    request = client.structure(raw_request, client.task.TaskPatch)
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
    request = client.structure(raw_request, client.task.TaskPatch)
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
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task_overlap_or_min('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_overlap_or_min('task-1', infinite_overlap=True)
    assert raw_result == client.unstructure(result)
