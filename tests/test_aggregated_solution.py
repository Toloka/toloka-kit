import asyncio
import json
from urllib.parse import urlparse, parse_qs

import httpx
import pytest
import toloka.client as client
from httpx import QueryParams

from .testutils.util_functions import check_headers


def test_aggregate_solution_by_pool(respx_mock, toloka_client, toloka_url):

    raw_request = {
        'type': 'WEIGHTED_DYNAMIC_OVERLAP',
        'pool_id': '21',
        'answer_weight_skill_id': '42',
        'fields': [{'name': 'out1'}]
    }

    operation_map = {
        'id': 'aggregated-solution-op1id',
        'type': 'SOLUTION.AGGREGATE',
        'status': 'RUNNING',
        'submitted': '2016-03-07T15:47:00',
        'started': '2016-03-07T15:47:21',
        'parameters': {'pool_id': '21'}
    }

    operation_success_map = dict(operation_map, status='SUCCESS', finished='2016-03-07T15:48:03')

    def aggregate_by_pool(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'aggregate_solutions_by_pool',
            'X-Low-Level-Method': 'aggregate_solutions_by_pool',
        }
        check_headers(request, expected_headers)

        assert raw_request == json.loads(request.content)
        return httpx.Response(status_code=202, json=operation_map)

    def operation_success(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'wait_operation',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)
        return httpx.Response(status_code=200, json=operation_success_map)

    respx_mock.post(f'{toloka_url}/aggregated-solutions/aggregate-by-pool').mock(side_effect=aggregate_by_pool)
    respx_mock.get(f'{toloka_url}/operations/aggregated-solution-op1id').mock(side_effect=operation_success)

    # Request object syntax
    request = client.structure(raw_request, client.aggregation.PoolAggregatedSolutionRequest)
    operation = toloka_client.aggregate_solutions_by_pool(request)
    operation = toloka_client.wait_operation(operation)
    assert operation_success_map == client.unstructure(operation)

    # Expanded syntax
    operation = toloka_client.aggregate_solutions_by_pool(
        type=client.aggregation.AggregatedSolutionType.WEIGHTED_DYNAMIC_OVERLAP,
        pool_id='21',
        answer_weight_skill_id='42',
        fields=[client.aggregation.PoolAggregatedSolutionRequest.Field(name='out1')]
    )
    operation = toloka_client.wait_operation(operation)
    assert operation_success_map == client.unstructure(operation)


def test_aggregatte_solution_by_task(respx_mock, toloka_client, toloka_url):
    raw_request = {
        'type': 'WEIGHTED_DYNAMIC_OVERLAP',
        'pool_id': '21',
        'task_id': 'qwerty-123',
        'answer_weight_skill_id': '42',
        'fields': [{'name': 'out1'}],
    }

    raw_result = {
        'pool_id': '21',
        'task_id': 'qwerty-123',
        'confidence': 0.42,
        'output_values': {'out1': True},
    }

    def aggregate_by_task(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'aggregate_solutions_by_task',
            'X-Low-Level-Method': 'aggregate_solutions_by_task',
        }
        check_headers(request, expected_headers)

        assert raw_request == json.loads(request.content)
        return httpx.Response(status_code=200, json=raw_result)

    respx_mock.post(f'{toloka_url}/aggregated-solutions/aggregate-by-task').mock(side_effect=aggregate_by_task)

    # Request object syntax
    request = client.structure(raw_request, client.aggregation.WeightedDynamicOverlapTaskAggregatedSolutionRequest)
    result = toloka_client.aggregate_solutions_by_task(request)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.aggregate_solutions_by_task(
        pool_id='21',
        task_id='qwerty-123',
        answer_weight_skill_id='42',
        fields=[client.aggregation.PoolAggregatedSolutionRequest.Field(name='out1')],
    )
    assert raw_result == client.unstructure(result)


def test_find_aggregated_solutions(respx_mock, toloka_client_with_expected_header, toloka_url):
    toloka_client, client_header = toloka_client_with_expected_header
    raw_result = {
        'has_more': False,
        'items': [
            {
                'pool_id': '21',
                'task_id': 'qwerty-234',
                'confidence': 0.41,
                'output_values': {'out1': True},
            },
            {
                'pool_id': '21',
                'task_id': 'qwerty-876',
                'confidence': 0.42,
                'output_values': {'out1': False},
            },
        ]
    }

    def aggregated_solutions(request):
        expected_headers = {
            'X-Caller-Context': client_header,
            'X-Top-Level-Method': 'find_aggregated_solutions',
            'X-Low-Level-Method': 'find_aggregated_solutions',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            task_id_gte=['qwerty_123'],
            task_id_lte=['qwerty_987'],
            sort=['-task_id'],
            limit=['42'],
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/aggregated-solutions/op_id').mock(side_effect=aggregated_solutions)

    # Request object syntax
    request = client.search_requests.AggregatedSolutionSearchRequest(
        task_id_gte='qwerty_123',
        task_id_lte='qwerty_987',
    )
    sort = client.search_requests.AggregatedSolutionSortItems(['-task_id'])
    result = toloka_client.find_aggregated_solutions('op_id', request, sort=sort, limit=42)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_aggregated_solutions(
        'op_id',
        task_id_gte='qwerty_123',
        task_id_lte='qwerty_987',
        sort=['-task_id'],
        limit=42,
    )
    assert raw_result == client.unstructure(result)


def test_get_aggregated_solutions(respx_mock, toloka_client, toloka_url):
    backend_solutions = [
        {
            'pool_id': '11',
            'task_id': '111',
            'output_values': {'out1': True},
            'confidence': 0.111
        },
        {
            'pool_id': '11',
            'task_id': '112',
            'output_values': {'out1': True},
            'confidence': 0.112
        },
        {
            'pool_id': '11',
            'task_id': '113',
            'output_values': {'out1': True},
            'confidence': 0.113
        },
        {
            'pool_id': '11',
            'task_id': '114',
            'output_values': {'out1': True},
            'confidence': 0.114
        },
        {
            'pool_id': '11',
            'task_id': '115',
            'output_values': {'out1': True},
            'confidence': 0.115
        }
    ]

    def find_aggregated_solutions_mock(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_aggregated_solutions',
            'X-Low-Level-Method': 'find_aggregated_solutions',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        task_id_gt = params.get('task_id_gt', None)
        params = params.remove('task_id_gt')
        assert QueryParams(sort=['task_id']) == params, params
        solutions_greater = [
            item
            for item in backend_solutions
            if task_id_gt is None or item['task_id'] > task_id_gt
        ][:2]  # For test purposes return 2 items at a time.
        has_more = (solutions_greater[-1]['task_id'] != backend_solutions[-1]['task_id'])
        return httpx.Response(status_code=200, json={'items': solutions_greater, 'has_more': has_more})

    respx_mock.get(f'{toloka_url}/aggregated-solutions/some_op_id').mock(side_effect=find_aggregated_solutions_mock)
    assert backend_solutions == client.unstructure(list(toloka_client.get_aggregated_solutions('some_op_id')))
