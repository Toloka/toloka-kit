from urllib.parse import urlparse, parse_qs

import toloka.client as client

from .testutils.util_functions import check_headers


def test_aggregate_solution_by_pool(requests_mock, toloka_client, toloka_url):

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

    def aggregate_by_pool(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'aggregate_solutions_by_pool',
            'X-Low-Level-Method': 'aggregate_solutions_by_pool',
        }
        check_headers(request, expected_headers)

        assert raw_request == request.json()
        return operation_map

    def operation_success(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'wait_operation',
            'X-Low-Level-Method': 'get_operation',
        }
        check_headers(request, expected_headers)

        return operation_success_map

    requests_mock.post(
        f'{toloka_url}/aggregated-solutions/aggregate-by-pool',
        json=aggregate_by_pool,
        status_code=202
    )
    requests_mock.get(
        f'{toloka_url}/operations/aggregated-solution-op1id',
        json=operation_success,
        status_code=200
    )

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


def test_aggregatte_solution_by_task(requests_mock, toloka_client, toloka_url):
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

    def aggregate_by_task(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'aggregate_solutions_by_task',
            'X-Low-Level-Method': 'aggregate_solutions_by_task',
        }
        check_headers(request, expected_headers)

        assert raw_request == request.json()
        return raw_result

    requests_mock.post(
        f'{toloka_url}/aggregated-solutions/aggregate-by-task',
        json=aggregate_by_task,
        status_code=200,
    )

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


def test_find_aggregated_solutions(requests_mock, toloka_client, toloka_url):
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

    def aggregated_solutions(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_aggregated_solutions',
            'X-Low-Level-Method': 'find_aggregated_solutions',
        }
        check_headers(request, expected_headers)

        assert {
            'task_id_gte': ['qwerty_123'],
            'task_id_lte': ['qwerty_987'],
            'sort': ['-task_id'],
            'limit': ['42'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(
        f'{toloka_url}/aggregated-solutions/op_id',
        json=aggregated_solutions,
        status_code=200,
    )

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


def test_get_aggregated_solutions(requests_mock, toloka_client, toloka_url):
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

    def find_aggregated_solutions_mock(request, _):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_aggregated_solutions',
            'X-Low-Level-Method': 'find_aggregated_solutions',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        task_id_gt = params.pop('task_id_gt', None)
        assert {'sort': ['task_id']} == params, params
        solutions_greater = [
            item
            for item in backend_solutions
            if task_id_gt is None or item['task_id'] > task_id_gt[0]
        ][:2]  # For test purposes return 2 items at a time.
        has_more = (solutions_greater[-1]['task_id'] != backend_solutions[-1]['task_id'])
        return {'items': solutions_greater, 'has_more': has_more}

    requests_mock.get(f'{toloka_url}/aggregated-solutions/some_op_id',
                      json=find_aggregated_solutions_mock,
                      status_code=200)
    assert backend_solutions == client.unstructure(list(toloka_client.get_aggregated_solutions('some_op_id')))
