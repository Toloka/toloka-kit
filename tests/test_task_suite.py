import datetime
import re
from operator import itemgetter
from typing import List

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client.exceptions import IncorrectActionsApiError

from .testutils.util_functions import check_headers


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


def test_create_task_suite(respx_mock, toloka_client, toloka_url, task_suite_map, task_suite_map_with_readonly):

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
    result = toloka_client.create_task_suite(client.unstructure(task_suite_map))
    assert task_suite_map_with_readonly == client.unstructure(result)


def test_create_task_suites(respx_mock, toloka_client, toloka_url):
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
        'validation_errors': {},
    }


def test_create_task_suites_sync_through_async(
        respx_mock, toloka_client, toloka_url, no_uuid_random,
        task_suites_map, operation_running_map, operation_success_map,
        create_log, get_task_suites_map, task_suites_result_map
):

    def check_task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites',
            'X-Low-Level-Method': 'create_task_suites',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id='operation-i1d',
            skip_invalid_items='true',
            allow_defaults='true',
            open_pool='true',
            async_mode='true'
        ) == request.url.params
        imcoming_task_suites = []
        for t in simplejson.loads(request.content):
            assert '__client_uuid' in t
            t.pop('__client_uuid')
            imcoming_task_suites.append(t)
        assert task_suites_map == imcoming_task_suites
        return httpx.Response(json=operation_running_map, status_code=201)

    def operation_success(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=operation_success_map, status_code=201)

    def get_log(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites',
            'X-Low-Level-Method': 'get_operation_log',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=create_log, status_code=201)

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites',
            'X-Low-Level-Method': 'find_task_suites',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json={'items': get_task_suites_map, 'has_more': False}, status_code=201)

    # mocks
    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=check_task_suites)
    respx_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}').mock(side_effect=operation_success)
    respx_mock.get(f'{toloka_url}/operations/{operation_running_map["id"]}/log').mock(side_effect=get_log)
    respx_mock.get(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    # Expanded syntax
    result = toloka_client.create_task_suites(
        [client.structure(t, client.task_suite.TaskSuite) for t in task_suites_map],
        operation_id='operation-i1d',
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert task_suites_result_map == client.unstructure(result)


def test_create_task_suites_async(respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map):
    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_task_suites_async',
            'X-Low-Level-Method': 'create_task_suites_async',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            skip_invalid_items='true',
            allow_defaults='true',
            open_pool='true',
            async_mode='true',
            operation_id=request.url.params['operation_id']
        ) == request.url.params
        assert task_suites_map == simplejson.loads(request.content)
        return httpx.Response(json=operation_success_map, status_code=200)

    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    request = client.structure(task_suites_map, List[client.task_suite.TaskSuite])

    # Request object syntax
    parameters = client.task_suite.TaskSuiteCreateRequestParameters(
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    result = toloka_client.create_task_suites_async(request, parameters)
    assert operation_success_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_task_suites_async(
        request,
        skip_invalid_items=True,
        allow_defaults=True,
        open_pool=True,
    )
    assert operation_success_map == client.unstructure(result)


def test_create_task_suites_retry_sync_through_async(
    respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map, create_log, no_uuid_random,
    get_task_suites_map
):
    requests_count = 0
    first_request_op_id = None

    def check_task_suites(request):
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

    def get_log(request):
        return httpx.Response(json=create_log, status_code=201)

    def task_suites(request):
        return httpx.Response(json={'items': get_task_suites_map, 'has_more': False}, status_code=201)

    respx_mock.get(
        url__regex=rf'{toloka_url}/operations/.*(?<!log)$'
    ).mock(httpx.Response(json=operation_success_map, status_code=200))
    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=check_task_suites)
    respx_mock.get(url__regex=rf'{toloka_url}/operations/.*/log').mock(side_effect=get_log)
    respx_mock.get(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    # Operations API should be mocked for create_tasks to work. This test checks retrying of the first request
    toloka_client.create_task_suites(
        task_suites=[client.structure(task_suite, client.TaskSuite) for task_suite in task_suites_map]
    )

    assert requests_count == 2


def test_create_task_suites_async_retry(respx_mock, toloka_client, toloka_url, task_suites_map, operation_success_map):
    requests_count = 0
    first_request_op_id = None

    def task_suites(request):
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
    respx_mock.post(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    # Operations API should be mocked for create_tasks to work. This test checks retrying of the first request
    toloka_client.create_task_suites_async(
        task_suites=[client.structure(task_suite, client.TaskSuite) for task_suite in task_suites_map]
    )

    assert requests_count == 2



def test_find_task_suites(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    raw_result = {'items': [task_suite_map_with_readonly], 'has_more': False}

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_task_suites',
            'X-Low-Level-Method': 'find_task_suites',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            pool_id='21',
            created_lte='2020-02-01T00:00:00',
            overlap_gte='42',
            sort='-created',
            limit='100',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/task-suites').mock(side_effect=task_suites)

    # Request object syntax
    request = client.search_requests.TaskSuiteSearchRequest(
        pool_id='21',
        created_lte=datetime.datetime(2020, 2, 1, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    sort = client.search_requests.TaskSuiteSortItems(['-created'])
    result = toloka_client.find_task_suites(request, sort=sort, limit=100)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_task_suites(
        pool_id='21',
        created_lte=datetime.datetime(2020, 2, 1, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
        sort=['-created'],
        limit=100,
    )
    assert raw_result == client.unstructure(result)


def test_get_task_suites(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    task_suites = [dict(task_suite_map_with_readonly, id=f'task-suite-i{i}d') for i in range(50)]
    task_suites.sort(key=itemgetter('id'))

    def get_task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_task_suites',
            'X-Low-Level-Method': 'find_task_suites',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params.get('id_gt', None)
        params = params.remove('id_gt')
        assert QueryParams(
            pool_id='21',
            created_lte='2020-02-01T00:00:00',
            overlap_gte='42',
            sort='id',
        ) == params

        items = [task_suite for task_suite in task_suites if id_gt is None or task_suite['id'] > id_gt][:3]
        return httpx.Response(json={'items': items, 'has_more': items[-1]['id'] != task_suites[-1]['id']}, status_code=200)

    respx_mock.get(f'{toloka_url}/task-suites').mock(side_effect=get_task_suites)

    # Request object syntax
    request = client.search_requests.TaskSuiteSearchRequest(
        pool_id='21',
        created_lte=datetime.datetime(2020, 2, 1, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    result = toloka_client.get_task_suites(request)
    assert task_suites == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_task_suites(
        pool_id='21',
        created_lte=datetime.datetime(2020, 2, 1, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    assert task_suites == client.unstructure(list(result))


def test_get_task_suite(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    def task_suite(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_task_suite',
            'X-Low-Level-Method': 'get_task_suite',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=task_suite_map_with_readonly, status_code=200)

    respx_mock.get(f'{toloka_url}/task-suites/task-suite-i1d').mock(side_effect=task_suite)
    result = toloka_client.get_task_suite('task-suite-i1d')
    assert task_suite_map_with_readonly == client.unstructure(result)


def test_patch_task_suite(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):
    raw_request = {'overlap': 12, 'infinite_overlap': False, 'issuing_order_override': 10.4}
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12, 'issuing_order_override': 10.4}

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task_suite',
            'X-Low-Level-Method': 'patch_task_suite',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d').mock(side_effect=task_suites)

    # Request object syntax
    patch = client.structure(raw_request, client.task_suite.TaskSuitePatch)
    result = toloka_client.patch_task_suite('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)


def test_patch_task_suite_with_parameters(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12, 'infinite_overlap': False}

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task_suite',
            'X-Low-Level-Method': 'patch_task_suite',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        assert QueryParams(open_pool='true') == params
        assert {'overlap': 12, 'infinite_overlap': False} == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d').mock(side_effect=task_suites)

    # Request object syntax
    patch = client.task_suite.TaskSuitePatch(overlap=12, open_pool=True)
    result = toloka_client.patch_task_suite('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_suite('task-suite-i1d', overlap=12, open_pool=True)
    assert raw_result == client.unstructure(result)


def test_patch_task_suite_overlap_or_min(respx_mock, toloka_client, toloka_url, task_suite_map_with_readonly):

    raw_patch = {'overlap': 10}
    raw_result = {**task_suite_map_with_readonly, 'overlap': 12}

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task_suite_overlap_or_min',
            'X-Low-Level-Method': 'patch_task_suite_overlap_or_min',
        }
        check_headers(request, expected_headers)

        assert raw_patch == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/task-suites/task-suite-i1d/set-overlap-or-min').mock(side_effect=task_suites)

    # Request object syntax
    patch = client.structure(raw_patch, client.task_suite.TaskSuiteOverlapPatch)
    result = toloka_client.patch_task_suite_overlap_or_min('task-suite-i1d', patch)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_suite_overlap_or_min('task-suite-i1d', overlap=10)
    assert raw_result == client.unstructure(result)
