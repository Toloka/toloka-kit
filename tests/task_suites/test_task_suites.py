import datetime
from operator import itemgetter

import httpx
import simplejson
import toloka.client as client
from httpx import QueryParams

from ..testutils.util_functions import check_headers


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
