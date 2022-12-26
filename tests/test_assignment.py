from datetime import datetime, timezone
from operator import itemgetter
from urllib.parse import urlparse, parse_qs
from decimal import Decimal

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams

from .testutils.util_functions import check_headers


@pytest.fixture
def assignment_map():
    return {
        'id': 'assignment-i1d',
        'task_suite_id': 'task-suite-i1d',
        'pool_id': '21',
        'user_id': 'user-i1d',
        'status': 'ACCEPTED',
        'reward': Decimal('0.05'),
        'bonus_ids': ['reward_id_1', 'reward_id_2'],
        'mixed': True,
        'automerged': True,
        'created': '2015-12-15T14:52:00',
        'submitted': '2015-12-15T15:10:00',
        'accepted': '2015-12-15T20:00:00',
        'tasks': [{'pool_id': '21', 'input_values': {'image': 'http://images.com/1.png'}, 'origin_task_id': '42'}],
        'first_declined_solution_attempt': [{'output_values': {'color': 'black', 'comment': 'So белый'}}],
        'solutions': [{'output_values': {'color': 'white', 'comment': 'So белый'}}],
        'owner': {
            'id': 'ac1e4701364b4ccef8a4fe10a8980cff',
            'myself': True,
        }
    }


def test_get_assignment(respx_mock, toloka_client, toloka_url, assignment_map):

    def get_assignment(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_assignment',
            'X-Low-Level-Method': 'get_assignment',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(assignment_map), status_code=200)

    respx_mock.get(f'{toloka_url}/assignments/assignment-i1d').mock(side_effect=get_assignment)
    result = toloka_client.get_assignment('assignment-i1d')
    assert assignment_map == client.unstructure(result)


def test_find_assignments(respx_mock, toloka_client, toloka_url, assignment_map):
    raw_result = {
        'items': [assignment_map],
        'has_more': False,
    }

    def find_assignments(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_assignments',
            'X-Low-Level-Method': 'find_assignments',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            status='ACCEPTED',
            pool_id='21',
            user_id='user-i1d',
            created_gte='2015-12-01T00:00:00',
            created_lt='2016-06-01T00:00:00',
            sort='-submitted',
        ) == request.url.params
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.get(f'{toloka_url}/assignments').mock(side_effect=find_assignments)

    # Request object syntax
    request = client.search_requests.AssignmentSearchRequest(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1, tzinfo=timezone.utc),
        created_lt=datetime(2016, 6, 1, tzinfo=timezone.utc),
    )
    sort = client.search_requests.AssignmentSortItems(['-submitted'])
    result = toloka_client.find_assignments(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_assignments(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1, tzinfo=timezone.utc),
        created_lt=datetime(2016, 6, 1, tzinfo=timezone.utc),
        sort=['-submitted']
    )
    assert raw_result == client.unstructure(result)


def test_get_assignments(respx_mock, toloka_client, toloka_url, assignment_map):
    assignments = [dict(assignment_map, id=f'assignment-i{i}d') for i in range(50)]
    assignments.sort(key=itemgetter('id'))

    def get_assignments(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_assignments',
            'X-Low-Level-Method': 'find_assignments',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params.get('id_gt', None)
        params = params.remove('id_gt')
        assert QueryParams(
            status='ACCEPTED',
            pool_id='21',
            user_id='user-i1d',
            created_gte='2015-12-01T00:00:00',
            created_lt='2016-06-01T00:00:00',
            sort='id',
        ) == params

        items = [assignment for assignment in assignments if id_gt is None or assignment['id'] > id_gt][:3]
        return httpx.Response(
            text=simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != assignments[-1]['id']}),
            status_code=200
        )

    respx_mock.get(f'{toloka_url}/assignments').mock(side_effect=get_assignments)

    # Request object syntax
    request = client.search_requests.AssignmentSearchRequest(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1, tzinfo=timezone.utc),
        created_lt=datetime(2016, 6, 1, tzinfo=timezone.utc),
    )
    result = toloka_client.get_assignments(request)
    assert assignments == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_assignments(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1, tzinfo=timezone.utc),
        created_lt=datetime(2016, 6, 1, tzinfo=timezone.utc),
    )
    assert assignments == client.unstructure(list(result))


def test_assignment_from_json(assignment_map):
    assignment = client.structure(assignment_map, client.assignment.Assignment)
    assignment_json = simplejson.dumps(assignment_map, use_decimal=True, ensure_ascii=True)
    assignment_from_json = client.assignment.Assignment.from_json(assignment_json)
    assert assignment == assignment_from_json


def test_assignment_to_json(assignment_map):
    assignment = client.structure(assignment_map, client.assignment.Assignment)
    assignment_json = assignment.to_json()
    assignment_json_basic = simplejson.dumps(assignment_map, use_decimal=True, ensure_ascii=True)
    assert simplejson.loads(assignment_json) == simplejson.loads(assignment_json_basic)


@pytest.mark.parametrize(
    ['raw_result', 'input_status'],
    [
        ({'status': 'ACCEPTED', 'pool_id': '21'}, client.assignment.Assignment.ACCEPTED),
        ({'status': 'ACCEPTED', 'pool_id': '21'}, 'ACCEPTED'),
        ({'status': 'ACCEPTED,SUBMITTED', 'pool_id': '21'}, [client.assignment.Assignment.ACCEPTED, client.assignment.Assignment.SUBMITTED]),
        ({'status': 'ACCEPTED,SUBMITTED', 'pool_id': '21'}, 'ACCEPTED, SUBMITTED'),
        ({'status': 'ACCEPTED,SUBMITTED', 'pool_id': '21'}, ['ACCEPTED', 'SUBMITTED']),
        ({'pool_id': '21'}, None),
    ]
)
def test_assignments_search_request(input_status, raw_result):
    request = client.search_requests.AssignmentSearchRequest(status=input_status, pool_id='21')
    assert client.unstructure(request) == raw_result

    request = client.search_requests.AssignmentSearchRequest(pool_id='21')
    request.status = input_status
    assert client.unstructure(request) == raw_result


def test_patch_assignment(respx_mock, toloka_client, toloka_url, assignment_map):
    raw_request = {
        'status': 'ACCEPTED',
        'public_comment': 'Well done',
    }

    raw_result = dict(assignment_map, public_comment='Well done')

    def patch_assignment(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'patch_assignment',
            'X-Low-Level-Method': 'patch_assignment',
        }
        check_headers(request, expected_headers)

        assert raw_request == simplejson.loads(request.content)
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.patch(f'{toloka_url}/assignments/assignment-i1d').mock(side_effect=patch_assignment)

    assignment_patch = client.assignment.AssignmentPatch(status=client.assignment.Assignment.ACCEPTED, public_comment='Well done')

    result = toloka_client.patch_assignment('assignment-i1d', assignment_patch)
    assert raw_result == client.unstructure(result)


@pytest.mark.parametrize(
    'value_to_check',
    [
        Decimal('0.05'),
        Decimal('0.0005'),
    ],
)
def test_reward_in_get_assignment(respx_mock, toloka_client, toloka_url, assignment_map, value_to_check):
    new_assignment_map = dict(assignment_map, reward=value_to_check)

    def get_assignment(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_assignment',
            'X-Low-Level-Method': 'get_assignment',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(new_assignment_map), status_code=200)

    respx_mock.get(f'{toloka_url}/assignments/assignment-i1d').mock(side_effect=get_assignment)
    result = toloka_client.get_assignment('assignment-i1d')
    assert result.reward == value_to_check
