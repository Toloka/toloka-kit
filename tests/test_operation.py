from datetime import datetime, timezone
from operator import itemgetter
from urllib.parse import parse_qs, urlparse

import pytest
import simplejson
import toloka.client as client

from toloka.client.operations import Operation, OperationType
from .testutils.util_functions import check_headers


@pytest.fixture()
def operation_map():
    return {
         'id': '123',
         'status': 'SUCCESS',
         'submitted': '2022-07-07T12:31:54.862000',
         'parameters': {
             'value': [
                 {
                     'name': 'completion_percentage',
                     'subject': 'POOL',
                     'subject_id': '123'
                 }
             ]
         },
         'started': '2022-07-07T12:31:55.370000',
         'finished': '2022-07-07T12:31:55.937000',
         'progress': 100,
         'details': {
             'value': [
                 {
                     'result': {
                         'type': 'NORMAL',
                         'value': 99,
                         'infinite': False,
                         'approximate': False
                     },
                    'request': {
                        'name': 'completion_percentage',
                        'subject': 'POOL',
                        'subject_id': '123'
                    },
                    'finished': '2022-07-07T12:31:55.599'
                 }
             ]
         },
         'type': 'ANALYTICS'
    }


def test_find_operations(requests_mock, toloka_client, toloka_url, operation_map):
    raw_result = {
        'items': [operation_map],
        'has_more': False,
    }

    def find_operations(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_operations',
            'X-Low-Level-Method': 'find_operations',
        }
        check_headers(request, expected_headers)

        assert {
            'status': ['SUCCESS'],
            'type': ['ANALYTICS'],
            'submitted_gte': ['2022-07-07T00:00:00'],
            'sort': ['-submitted'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_url}/operations', text=find_operations)

    # Request object syntax
    request = client.search_requests.OperationSearchRequest(
        status=Operation.Status.SUCCESS,
        type=OperationType.ANALYTICS,
        submitted_gte=datetime(2022, 7, 7, tzinfo=timezone.utc),
    )
    sort = client.search_requests.OperationSortItems(['-submitted'])
    result = toloka_client.find_operations(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_operations(
        status=Operation.Status.SUCCESS,
        type=OperationType.ANALYTICS,
        submitted_gte=datetime(2022, 7, 7, tzinfo=timezone.utc),
        sort=['-submitted']
    )
    assert raw_result == client.unstructure(result)


def test_get_operations(requests_mock, toloka_client, toloka_url, operation_map):
    operations = [dict(operation_map, id=f'operation-i{i}d') for i in range(50)]
    operations.sort(key=itemgetter('id'))

    def get_operations(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_operations',
            'X-Low-Level-Method': 'find_operations',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'status': ['SUCCESS'],
            'type': ['ANALYTICS'],
            'submitted_gte': ['2022-07-07T00:00:00'],
            'sort': ['id'],
        } == params

        items = [operation for operation in operations if id_gt is None or operation['id'] > id_gt][:3]
        return simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != operations[-1]['id']})

    requests_mock.get(f'{toloka_url}/operations', text=get_operations)

    # Request object syntax
    request = client.search_requests.OperationSearchRequest(
        status=Operation.Status.SUCCESS,
        type=OperationType.ANALYTICS,
        submitted_gte=datetime(2022, 7, 7, tzinfo=timezone.utc),
    )
    result = toloka_client.get_operations(request)
    assert operations == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_operations(
        status=Operation.Status.SUCCESS,
        type=OperationType.ANALYTICS,
        submitted_gte=datetime(2022, 7, 7, tzinfo=timezone.utc),
    )
    assert operations == client.unstructure(list(result))
