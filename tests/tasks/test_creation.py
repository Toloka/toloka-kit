import re
from uuid import UUID

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client import Task
from toloka.client.batch_create_results import TaskBatchCreateResult
from toloka.client.exceptions import FailedOperation, IncorrectActionsApiError
from toloka.client.operations import Operation, TasksCreateOperation

from ..testutils.util_functions import (
    assert_async_object_creation_is_successful, assert_retried_async_object_creation_returns_existing_operation,
    assert_retried_failed_operation_fails_with_failed_operation_exception,
    assert_retried_sync_via_async_object_creation_returns_already_existing_object,
    assert_sync_via_async_object_creation_is_successful, check_headers,
)


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
def operation_running_map_single_task():
    return {
        'id': '281073ea-ab34-416e-a028-47421ff1b166',
        'type': 'TASK.BATCH_CREATE',
        'status': 'RUNNING',
        'submitted': '2016-10-10T20:33:01',
        'started': '2016-10-10T23:33:00',
        'parameters': {'skip_invalid_items': True, 'allow_defaults': True, 'open_pool': True},
        'details': {'items_count': 1},
    }


@pytest.fixture
def operation_success_map_single_task(operation_running_map_single_task):
    return {**operation_running_map_single_task, 'status': 'SUCCESS'}


@pytest.fixture
def operation_fail_map_single_task(operation_running_map_single_task):
    return {**operation_running_map_single_task, 'status': 'FAIL'}


@pytest.fixture
def operation_running_map(operation_running_map_single_task):
    return {
        **operation_running_map_single_task,
        'details': {'items_count': 2},
    }


@pytest.fixture
def operation_success_map(operation_running_map):
    return {**operation_running_map, 'status': 'SUCCESS'}


@pytest.fixture
def operation_fail_map(operation_running_map):
    return {**operation_running_map, 'status': 'FAIL'}


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


def test_create_task_sync_through_async(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    tasks_map, operation_running_map_single_task, operation_success_map_single_task,
    create_tasks_log, created_tasks_21_map,
):
    task = tasks_map[0]
    create_task_log = create_tasks_log[:1]

    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task,
        create_method_kwargs={
            'task': Task.structure(task),
            'operation_id': UUID('281073ea-ab34-416e-a028-47421ff1b166'),
            'allow_defaults': True,
            'open_pool': True,
        },
        returned_object=created_tasks_21_map,
        expected_response_object=Task.structure(created_tasks_21_map),
        operation_log=create_task_log,
        create_object_path='tasks',
        get_object_path=f'tasks/{created_tasks_21_map["id"]}',
        operation_running=Operation.structure(operation_running_map_single_task),
        success_operation=Operation.structure(operation_success_map_single_task),
        expected_query_params={
            'operation_id': '281073ea-ab34-416e-a028-47421ff1b166',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
        },
        top_level_method_header='create_task',
        low_level_method_header='create_task',
    )


def test_create_task_sync_through_async_retry(
    respx_mock, toloka_client, toloka_url, tasks_map, operation_success_map_single_task, create_tasks_log,
    created_tasks_21_map,
):
    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task,
        create_method_kwargs={
            'task': Task.structure(tasks_map[0]),
        },
        returned_object=created_tasks_21_map,
        expected_response_object=Task.structure(created_tasks_21_map),
        create_object_path='tasks',
        get_object_path=f'tasks/{created_tasks_21_map["id"]}',
        operation_log=create_tasks_log[:1],
        success_operation_map=operation_success_map_single_task,
    )


def test_create_task_sync_through_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, tasks_map, operation_fail_map_single_task,
):
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task,
        create_method_kwargs={
            'task': Task.structure(tasks_map[0]),
        },
        create_object_path='tasks',
        failed_operation_map=operation_fail_map_single_task,
    )


def test_create_tasks_sync_through_async(
    respx_mock, toloka_client, toloka_url,
    tasks_map, operation_running_map, operation_success_map,
    create_tasks_log, created_tasks_21_map, created_tasks_22_map,
    task_create_result_map
):
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

    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map],
            'operation_id': UUID('281073ea-ab34-416e-a028-47421ff1b166'),
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        returned_object=return_tasks_by_pool,
        expected_response_object=TaskBatchCreateResult.structure(task_create_result_map),
        operation_log=create_tasks_log,
        create_object_path='tasks',
        get_object_path='tasks',
        operation_running=Operation.structure(operation_running_map),
        success_operation=Operation.structure(operation_success_map),
        expected_query_params={
            'operation_id': '281073ea-ab34-416e-a028-47421ff1b166',
            'skip_invalid_items': 'true',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
        },
        top_level_method_header='create_tasks',
        low_level_method_header='create_tasks',
    )


def test_create_tasks_sync_through_async_retry(
    respx_mock, toloka_client, toloka_url, tasks_map, task_create_result_map, operation_success_map, create_tasks_log,
    created_tasks_21_map, created_tasks_22_map,
):
    def return_tasks_by_pool(request):
        params = request.url.params
        res_map = [created_tasks_21_map] if params['pool_id'] == '21' else [created_tasks_22_map]
        return httpx.Response(json={'items': res_map, 'has_more': False}, status_code=201)

    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map]
        },
        returned_object=return_tasks_by_pool,
        expected_response_object=TaskBatchCreateResult.structure(task_create_result_map),
        create_object_path='tasks',
        get_object_path='tasks',
        operation_log=create_tasks_log,
        success_operation_map=operation_success_map
    )


def test_create_tasks_sync_through_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, tasks_map, operation_fail_map,
):
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map],
        },
        create_object_path='tasks',
        failed_operation_map=operation_fail_map,
    )


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
    assert_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks_async,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map],
            'operation_id': UUID('281073ea-ab34-416e-a028-47421ff1b166'),
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        create_object_path='tasks',
        success_operation_map=create_tasks_operation_map,
        expected_query_params={
            'operation_id': '281073ea-ab34-416e-a028-47421ff1b166',
            'skip_invalid_items': 'true',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
        },
        top_level_method_header='create_tasks_async',
        low_level_method_header='create_tasks_async',
    )


def test_create_tasks_async_retry(
    respx_mock, toloka_client, toloka_url, tasks_map, operation_success_map
):
    assert_retried_async_object_creation_returns_existing_operation(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks_async,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map]
        },
        create_object_path='tasks',
        success_operation_map=operation_success_map
    )


def test_create_tasks_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, tasks_map, operation_fail_map
):
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_tasks_async,
        create_method_kwargs={
            'tasks': [client.structure(task, client.task.Task) for task in tasks_map]
        },
        create_object_path='tasks',
        failed_operation_map=operation_fail_map,
    )

