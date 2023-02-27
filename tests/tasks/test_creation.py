import re

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client.exceptions import IncorrectActionsApiError

from ..testutils.util_functions import check_headers


# TEST SYNC CREATION

def test_create_task_sync(respx_mock, toloka_client, toloka_url, task_map, task_map_with_readonly):

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task',
            'X-Low-Level-Method': 'create_task',
        }
        check_headers(request, expected_headers)

        assert task_map == simplejson.loads(request.content)
        return httpx.Response(json=task_map_with_readonly, status_code=201)

    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)
    result = toloka_client.create_task(client.structure(task_map, client.task.Task), async_mode=False)
    assert task_map_with_readonly == client.unstructure(result)


@pytest.fixture
def tasks_map():
    return [
        {'pool_id': '21', 'input_values': {'image': 'http://images.com/1.png'}},
        {'pool_id': '22', 'input_values': {'image': 'http://images.com/2.png'}},
        {'pool_id': '22', 'input_values': {'imagis': 'http://images.com/3.png'}}
    ]


def test_create_tasks_with_error(respx_mock, toloka_client, toloka_url, task_map, task_map_with_readonly):
    tasks_map = [task_map, {'pool_id': '21', 'input_values': {'image': None}}]
    raw_result = {
        'items': {'0': task_map_with_readonly},
        'validation_errors': {
            '1': {'input_values.image': {'code': 'VALUE_REQUIRED', 'message': 'May not be null'}},
        }
    }

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'create_tasks',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            allow_defaults='true', async_mode='false', operation_id=request.url.params['operation_id']
        ) == request.url.params
        assert tasks_map == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=201)

    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)

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
def created_tasks_21_map():
    return {
        'id': '00014495f0--60213f7c25a8b84e2ffb7a2c',
        'pool_id': '21',
        'input_values': {'image': 'http://images.com/1.png'},
        'overlap': 1,
        'infinite_overlap': False,
        'remaining_overlap': 1,
    }


@pytest.fixture
def created_tasks_22_map():
    return {
        'id': '00014495f0--60213f7c25a8b84e2ffb7a3b',
        'pool_id': '22',
        'input_values': {'image': 'http://images.com/2.png'},
        'overlap': 1,
        'infinite_overlap': False,
        'remaining_overlap': 1,
    }


@pytest.fixture
def task_create_result_map(created_tasks_21_map, created_tasks_22_map):
    return {
        'items': {
            '0': created_tasks_21_map,
            '1': created_tasks_22_map,
        },
        'validation_errors': {
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


def test_create_tasks_sync(respx_mock, toloka_client, toloka_url, tasks_map, task_create_result_map):

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'create_tasks',
        }
        check_headers(request, expected_headers)

        assert tasks_map == simplejson.loads(request.content)
        return httpx.Response(json=task_create_result_map, status_code=201)

    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        skip_invalid_items=True,
        allow_defaults=True,
        async_mode=False,
    )
    assert task_create_result_map == client.unstructure(result)


# TEST ASYNC CREATION


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
                '__item_idx': '0',
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
                '__item_idx': '1',
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
                '__item_idx': '2',
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
                'pool_id': 22,
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


def test_create_tasks_sync_through_async(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    tasks_map, operation_running_map, operation_success_map,
    create_tasks_log, created_tasks_21_map, created_tasks_22_map,
    task_create_result_map
):

    def check_tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'create_tasks',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id='281073ea-ab34-416e-a028-47421ff1b166',
            skip_invalid_items='true',
            allow_defaults='true',
            open_pool='true',
            async_mode='true',
        ) == request.url.params
        incoming_tasks = []
        for t in simplejson.loads(request.content):
            assert '__item_idx' in t
            t.pop('__item_idx')
            incoming_tasks.append(t)
        assert tasks_map == incoming_tasks
        return httpx.Response(json=operation_running_map, status_code=201)

    def operation_success(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=operation_success_map, status_code=201)

    def tasks_log(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'get_operation_log',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=create_tasks_log, status_code=201)

    def return_tasks_by_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks',
            'X-Low-Level-Method': 'find_tasks',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        res_map = [created_tasks_21_map] if params['pool_id'] == '21' else [created_tasks_22_map]
        return httpx.Response(json={'items': res_map, 'has_more': False}, status_code=201)

    # mocks
    # create_task -> operation
    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=check_tasks,)
    # wait_operation -> operation Success
    respx_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}').mock(side_effect=operation_success)
    # get_log -> log_res
    respx_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}/log').mock(side_effect=tasks_log)
    # get tasks from pools (2 calls - for each pool)
    respx_mock.get(f'{toloka_url}/tasks').mock(side_effect=return_tasks_by_pool)

    # Expanded syntax
    result = toloka_client.create_tasks(
        [client.structure(task, client.task.Task) for task in tasks_map],
        operation_id='281073ea-ab34-416e-a028-47421ff1b166',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert task_create_result_map == client.unstructure(result)


@pytest.fixture
def create_tasks_operation_map():
    return {
        'id': '281073ea-ab34-416e-a028-47421ff1b166',
        'type': 'TASK.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2016-10-10T20:33:01',
        'started': '2016-10-10T23:33:00',
        'parameters': {'skip_invalid_items': True, 'allow_defaults': True, 'open_pool': True},
        'details': {'items_count': 2},
    }


def test_create_tasks_async(respx_mock, toloka_client, toloka_url, tasks_map, create_tasks_operation_map):

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_tasks_async',
            'X-Low-Level-Method': 'create_tasks_async',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id='281073ea-ab34-416e-a028-47421ff1b166',
            skip_invalid_items='true',
            allow_defaults='true',
            open_pool='true',
            async_mode='true',
        ) == request.url.params
        assert tasks_map == simplejson.loads(request.content)
        return httpx.Response(json=create_tasks_operation_map, status_code=201)

    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)

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
    assert create_tasks_operation_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_tasks_async(
        [client.structure(task, client.task.Task) for task in tasks_map],
        operation_id='281073ea-ab34-416e-a028-47421ff1b166',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert create_tasks_operation_map == client.unstructure(result)


def test_create_tasks_retry_sync_through_async(
    respx_mock, toloka_client, toloka_url, tasks_map, task_create_result_map, operation_success_map, create_tasks_log,
    no_uuid_random, created_tasks_21_map, created_tasks_22_map,
):
    requests_count = 0
    first_request_op_id = None

    def tasks(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count += 1
        if requests_count == 1:
            first_request_op_id = request.url.params['operation_id']
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == first_request_op_id
        unstructured_error = client.unstructure(IncorrectActionsApiError(
            code='OPERATION_ALREADY_EXISTS',
        ))
        del unstructured_error['status_code']

        return httpx.Response(
            json=unstructured_error,
            status_code=409
        )

    def tasks_log(request):
        return httpx.Response(json=create_tasks_log, status_code=201)

    def return_tasks_by_pool(request):
        params = request.url.params
        res_map = [created_tasks_21_map] if params['pool_id'] == '21' else [created_tasks_22_map]
        return httpx.Response(json={'items': res_map, 'has_more': False}, status_code=201)

    respx_mock.get(
        url__regex=rf'{toloka_url}/operations/.*(?<!log)$'
    ).mock(httpx.Response(json=operation_success_map, status_code=200))
    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)
    respx_mock.get(re.compile(rf'{toloka_url}/operations/.*/log')).mock(side_effect=tasks_log)
    respx_mock.get(f'{toloka_url}/tasks').mock(side_effect=return_tasks_by_pool)

    result = toloka_client.create_tasks(
        tasks=[client.structure(task, client.task.Task) for task in tasks_map]
    )

    assert requests_count == 2
    assert task_create_result_map == client.unstructure(result)


def test_create_tasks_async_retry(
    respx_mock, toloka_client, toloka_url, tasks_map, task_create_result_map, operation_success_map
):
    requests_count = 0
    first_request_op_id = None

    def tasks(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count += 1
        if requests_count == 1:
            first_request_op_id = request.url.params['operation_id']
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == first_request_op_id
        unstructured_error = client.unstructure(
            IncorrectActionsApiError(
                code='OPERATION_ALREADY_EXISTS',
            )
        )
        del unstructured_error['status_code']

        return httpx.Response(
            json=unstructured_error,
            status_code=409
        )

    respx_mock.get(
        re.compile(rf'{toloka_url}/operations/.*')
    ).mock(httpx.Response(json=operation_success_map, status_code=200))
    respx_mock.post(f'{toloka_url}/tasks').mock(side_effect=tasks)

    result = toloka_client.create_tasks_async(
        tasks=[client.structure(task, client.task.Task) for task in tasks_map]
    )

    assert requests_count == 2
    assert operation_success_map == client.unstructure(result)
