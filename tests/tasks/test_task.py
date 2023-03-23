import datetime
from operator import itemgetter
from uuid import uuid4
import simplejson as json

import httpx
import simplejson
import toloka.client as client
from httpx import QueryParams

from ..testutils.util_functions import check_headers


def test_task_from_json(task_map):
    task = client.structure(task_map, client.task.Task)
    task_json = json.dumps(task_map, use_decimal=True, ensure_ascii=False)
    task_from_json = client.task.Task.from_json(task_json)
    assert task == task_from_json


def test_task_to_json(task_map):
    task = client.structure(task_map, client.task.Task)
    task_json = task.to_json()
    task_json_basic = json.dumps(task_map, use_decimal=True, ensure_ascii=False)
    assert json.loads(task_json) == json.loads(task_json_basic)


def test_find_tasks(respx_mock, toloka_client, toloka_url, task_map_with_readonly):

    raw_result = {'items': [task_map_with_readonly], 'has_more': False}

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_tasks',
            'X-Low-Level-Method': 'find_tasks',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            pool_id='21',
            created_gt='2001-01-01T12:00:00',
            overlap_gte='42',
            sort='id,-created',
            limit='20',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/tasks').mock(side_effect=tasks)

    # Request object syntax
    request = client.search_requests.TaskSearchRequest(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    sort = client.search_requests.TaskSortItems(['id', '-created'])
    result = toloka_client.find_tasks(request, sort=sort, limit=20)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_tasks(
        pool_id=21,
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
        sort=['id', '-created'],
        limit=20,
    )
    assert raw_result == client.unstructure(result)


def test_get_tasks(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    tasks = [dict(task_map_with_readonly, id=str(uuid4())) for _ in range(50)]
    tasks.sort(key=itemgetter('id'))

    def get_tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_tasks',
            'X-Low-Level-Method': 'find_tasks',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params.get('id_gt', None)
        params = params.remove('id_gt')
        assert QueryParams(
            pool_id='21',
            created_gt='2001-01-01T12:00:00',
            overlap_gte='42',
            sort='id',
        ) == params

        items = [task for task in tasks if id_gt is None or task['id'] > id_gt][:3]
        return httpx.Response(json={'items': items, 'has_more': items[-1]['id'] != tasks[-1]['id']}, status_code=200)

    respx_mock.get(f'{toloka_url}/tasks').mock(side_effect=get_tasks)

    # Request object syntax
    request = client.search_requests.TaskSearchRequest(
        pool_id='21',
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    result = toloka_client.get_tasks(request)
    assert tasks == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_tasks(
        pool_id='21',
        created_gt=datetime.datetime(2001, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        overlap_gte=42,
    )
    assert tasks == client.unstructure(list(result))


def test_get_task(respx_mock, toloka_client, toloka_url, task_map_with_readonly):

    def get_task(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_task',
            'X-Low-Level-Method': 'get_task',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=task_map_with_readonly, status_code=200)

    respx_mock.get(f'{toloka_url}/tasks/task-1').mock(side_effect=get_task)
    result = toloka_client.get_task('task-1')
    assert task_map_with_readonly == client.unstructure(result)


def test_patch_task(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'overlap': 10}
    raw_result = {**task_map_with_readonly, **raw_request}

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task',
            'X-Low-Level-Method': 'patch_task',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/tasks/task-1').mock(side_effect=tasks)

    # Request object syntax
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task('task-1', overlap=10)
    assert raw_result == client.unstructure(result)


def test_patch_task_with_baseline_solution(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {
        'baseline_solutions': [{
            'output_values': {'color': 'green'},
            'confidence_weight': 4.2,
        }]
    }
    raw_result = {**task_map_with_readonly, **raw_request}

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task',
            'X-Low-Level-Method': 'patch_task',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/tasks/task-1').mock(side_effect=tasks)

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


def test_patch_task_with_known_solutions(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {
        'known_solutions': [
            {
                'output_values': {'color': 'black'},
                'correctness_weight': 1.0,
            },
        ],
        'message_on_unknown_solution': 'Main color is black'
    }
    raw_result = {**task_map_with_readonly, **raw_request}

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task',
            'X-Low-Level-Method': 'patch_task',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/tasks/task-1').mock(side_effect=tasks)

    # Request object syntax
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task(
        'task-1',
        known_solutions=[
            client.task.Task.KnownSolution(
                output_values={'color': 'black'},
                correctness_weight=1.0,
            )
        ],
        message_on_unknown_solution='Main color is black',
    )
    assert raw_result == client.unstructure(result)


def test_task_overlap_or_min(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'overlap': 10}
    raw_result = {**task_map_with_readonly, 'overlap': 12}

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task_overlap_or_min',
            'X-Low-Level-Method': 'patch_task_overlap_or_min',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/tasks/task-1/set-overlap-or-min').mock(side_effect=tasks)

    # Request object syntax
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task_overlap_or_min('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_overlap_or_min('task-1', overlap=10)
    assert raw_result == client.unstructure(result)


def test_task_overlap_or_min_infinite_overlap(respx_mock, toloka_client, toloka_url, task_map_with_readonly):
    raw_request = {'infinite_overlap': True}
    raw_result = task_map_with_readonly

    def tasks(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_task_overlap_or_min',
            'X-Low-Level-Method': 'patch_task_overlap_or_min',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.patch(f'{toloka_url}/tasks/task-1/set-overlap-or-min').mock(side_effect=tasks)

    # Request object syntax
    request = client.structure(raw_request, client.task.TaskPatch)
    result = toloka_client.patch_task_overlap_or_min('task-1', request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.patch_task_overlap_or_min('task-1', infinite_overlap=True)
    assert raw_result == client.unstructure(result)
