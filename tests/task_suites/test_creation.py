import re
from typing import List

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client.batch_create_results import TaskSuiteBatchCreateResult
from toloka.client.exceptions import IncorrectActionsApiError
from toloka.client.operations import Operation

from ..testutils.util_functions import (
    assert_async_object_creation_is_successful, assert_retried_async_object_creation_returns_existing_operation,
    assert_sync_via_async_object_creation_is_successful,
    assert_retried_failed_operation_fails_with_failed_operation_exception,
    assert_retried_sync_via_async_object_creation_returns_already_existing_object, check_headers,
)


def test_create_task_suite_sync(respx_mock, toloka_client, toloka_url, task_suite_map, task_suite_map_with_readonly):

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suite',
            'X-Low-Level-Method': 'create_task_suite',
        }
        check_headers(request, expected_headers)

        assert task_suite_map == simplejson.loads(request.content)
        return httpx.Response(json=task_suite_map_with_readonly, status_code=200)

    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    # TODO: test creation parameters
    result = toloka_client.create_task_suite(client.unstructure(task_suite_map), async_mode=False)
    assert task_suite_map_with_readonly == client.unstructure(result)


def test_create_task_suites_sync(respx_mock, toloka_client, toloka_url):
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

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites',
            'X-Low-Level-Method': 'create_task_suites',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=201)

    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    task_suites_to_create = client.structure(raw_request, List[client.task_suite.TaskSuite])
    result = toloka_client.create_task_suites(task_suites_to_create, async_mode=False, skip_invalid_items=True)
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
def operation_running_map_single_task_suite():
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
        'details': {'items_count': 1},
    }


@pytest.fixture
def operation_success_map_single_task_suite(operation_running_map_single_task_suite):
    return {**operation_running_map_single_task_suite, 'status': 'SUCCESS'}


@pytest.fixture
def operation_fail_map_single_task_suite(operation_running_map_single_task_suite):
    return {**operation_running_map_single_task_suite, 'status': 'FAIL'}


@pytest.fixture
def operation_running_map(operation_running_map_single_task_suite):
    return {
        **operation_running_map_single_task_suite,
        'details': {'items_count': 2},
    }


@pytest.fixture
def operation_fail_map(operation_running_map):
    return {**operation_running_map, 'status': 'FAIL'}


@pytest.fixture
def operation_success_map(operation_running_map):
    return {**operation_running_map, 'status': 'SUCCESS'}


@pytest.fixture
def create_log():
    return [
        {
            'input': {
                'pool_id': '21',
                'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
                 '__item_idx': "0",
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
                '__item_idx': '1',
            },
            'output': {
                'task_suite_id': '00013b0abd--60094b06c680984b001e0072',
            },
            'success': True,
            'type': 'TASK_SUITE_CREATE',
        },
    ]


@pytest.fixture
def task_suite_1():
    return {
        'id': '00013b0abd--60094b06c680984b001e0071',
        'pool_id': '21',
        'tasks': [{'input_values': {'image': 'http://images.com/1.png'}}],
        'mixed': False,
        'created': '2016-07-09T14:39:00',
    }


@pytest.fixture
def task_suite_2():
    return {
            'id': '00013b0abd--60094b06c680984b001e0072',
            'pool_id': '21',
            'tasks': [{'input_values': {'image': 'http://images.com/2.png'}}],
            'mixed': False,
            'created': '2016-07-09T14:40:00',
        }


@pytest.fixture
def get_task_suites_map(task_suite_1, task_suite_2):
    return [task_suite_1, task_suite_2]


@pytest.fixture
def task_suites_result_map(task_suite_1, task_suite_2):
    return {
        'items': {
            '0': task_suite_1,
            '1': task_suite_2,
        },
        'validation_errors': {},
    }


def test_create_task_suite_sync_through_async(
        respx_mock, toloka_client, toloka_url, no_uuid_random,
        task_suites_map, operation_running_map_single_task_suite, operation_success_map_single_task_suite,
        create_log, task_suite_1,
):
    task_suite = client.task_suite.TaskSuite.structure(task_suites_map[0])
    create_log = create_log[:1]

    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suite,
        create_method_kwargs={
            'task_suite': task_suite,
            'operation_id': 'operation-i1d',
            'allow_defaults': True,
            'open_pool': True,
        },
        returned_object=task_suite_1,
        expected_response_object=client.task_suite.TaskSuite.structure(task_suite_1),
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path=f'task-suites/{task_suite_1["id"]}',
        operation_running=Operation.structure(operation_running_map_single_task_suite),
        success_operation=Operation.structure(operation_success_map_single_task_suite),
        expected_query_params={
            'operation_id': 'operation-i1d',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
        },
    )


def test_create_task_suite_sync_through_async_retry(
    respx_mock, toloka_client, toloka_url, no_uuid_random, task_suites_map, operation_success_map_single_task_suite,
    create_log, task_suite_1
):
    task_suite = task_suites_map[0]
    create_log = create_log[:1]

    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suite,
        create_method_kwargs={
            'task_suite': client.structure(task_suite, client.TaskSuite)
        },
        returned_object=task_suite_1,
        expected_response_object=client.structure(task_suite_1, client.TaskSuite),
        success_operation_map=operation_success_map_single_task_suite,
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path=f'task-suites/{task_suite_1["id"]}',
    )


def test_create_task_suite_sync_through_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, no_uuid_random, task_suites_map, operation_fail_map_single_task_suite,
    create_log, task_suite_1
):
    task_suite = task_suites_map[0]
    create_log = create_log[:1]

    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suite,
        create_method_kwargs={
            'task_suite': client.structure(task_suite, client.TaskSuite)
        },
        returned_object=task_suite_1,
        failed_operation_map=operation_fail_map_single_task_suite,
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path=f'task-suites/{task_suite_1["id"]}',
    )


def test_create_task_suites_sync_through_async(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    task_suites_map, operation_running_map, operation_success_map,
    create_log, get_task_suites_map, task_suites_result_map
):
    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suites,
        create_method_kwargs={
            'task_suites': [client.structure(t, client.task_suite.TaskSuite) for t in task_suites_map],
            'operation_id': 'operation-i1d',
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        returned_object={'items': get_task_suites_map, 'has_more': False},
        expected_response_object=TaskSuiteBatchCreateResult.structure(task_suites_result_map),
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path=f'task-suites',
        operation_running=Operation.structure(operation_running_map),
        success_operation=Operation.structure(operation_success_map),
        expected_query_params={
            'operation_id': 'operation-i1d',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
            'skip_invalid_items': 'true',
        },
    )


def test_create_task_suites_sync_through_async_retry(
    respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map, create_log, no_uuid_random,
    get_task_suites_map, task_suites_result_map
):
    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suites,
        create_method_kwargs={
            'task_suites': [client.structure(task_suite, client.TaskSuite) for task_suite in task_suites_map]
        },
        returned_object={'items': get_task_suites_map, 'has_more': False},
        expected_response_object=TaskSuiteBatchCreateResult.structure(task_suites_result_map),
        success_operation_map=operation_success_map,
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path='task-suites',
    )


def test_create_task_suites_sync_through_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    task_suites_map, operation_running_map, operation_fail_map,
    create_log, get_task_suites_map, task_suites_result_map
):
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suites,
        create_method_kwargs={
            'task_suites': [client.structure(t, client.task_suite.TaskSuite) for t in task_suites_map],
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        returned_object={'items': get_task_suites_map, 'has_more': False},
        failed_operation_map=operation_fail_map,
        operation_log=create_log,
        create_object_path='task-suites',
        get_object_path=f'task-suites',
    )


def test_create_task_suites_async(respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map):
    assert_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suites_async,
        create_method_kwargs={
            'task_suites': client.structure(task_suites_map, List[client.task_suite.TaskSuite]),
            'skip_invalid_items': True,
            'allow_defaults': True,
            'open_pool': True,
        },
        create_object_path='task-suites',
        success_operation_map=operation_success_map,
        expected_query_params={
            'skip_invalid_items': 'true',
            'allow_defaults': 'true',
            'open_pool': 'true',
            'async_mode': 'true',
        },
        top_level_method_header='create_task_suites_async',
        low_level_method_header='create_task_suites_async',
    )


def test_create_task_suites_async_retry(respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map):
    assert_retried_async_object_creation_returns_existing_operation(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_task_suites_async,
        create_method_kwargs={
            'task_suites': [client.structure(task_suite, client.TaskSuite) for task_suite in task_suites_map]
        },
        create_object_path='task-suites',
        success_operation_map=operation_success_map
    )
