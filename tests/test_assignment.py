from datetime import datetime
from operator import itemgetter
from urllib.parse import urlparse, parse_qs
from decimal import Decimal

import pytest
import simplejson
import toloka.client as client


@pytest.fixture
def assignment_map():
    return {
        'id': 'assignment-i1d',
        'task_suite_id': 'task-suite-i1d',
        'pool_id': '21',
        'user_id': 'user-i1d',
        'status': 'ACCEPTED',
        'reward': Decimal('0.05'),
        'mixed': True,
        'automerged': True,
        'created': '2015-12-15T14:52:00',
        'submitted': '2015-12-15T15:10:00',
        'accepted': '2015-12-15T20:00:00',
        'tasks': [{'pool_id': '21', 'input_values': {'image': 'http://images.com/1.png'}, 'origin_task_id': '42'}],
        'first_declined_solution_attempt': [{'output_values': {'color': 'black', 'comment': 'So white'}}],
        'solutions': [{'output_values': {'color' : 'white', 'comment': 'So white'}}],
    }


def test_get_assignment(requests_mock, toloka_client, toloka_url, assignment_map):
    requests_mock.get(f'{toloka_url}/assignments/assignment-i1d', text=simplejson.dumps(assignment_map))
    result = toloka_client.get_assignment('assignment-i1d')
    assert assignment_map == client.unstructure(result)


def test_find_assignments(requests_mock, toloka_client, toloka_url, assignment_map):
    raw_result = {
        'items': [assignment_map],
        'has_more': False,
    }

    def find_assignments(request, context):
        assert {
            'status': ['ACCEPTED'],
            'pool_id': ['21'],
            'user_id': ['user-i1d'],
            'created_gte': ['2015-12-01T00:00:00'],
            'created_lt': ['2016-06-01T00:00:00'],
            'sort': ['-submitted'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_url}/assignments', text=find_assignments)

    # Request object syntax
    request = client.search_requests.AssignmentSearchRequest(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1),
        created_lt=datetime(2016, 6, 1),
    )
    sort = client.search_requests.AssignmentSortItems(['-submitted'])
    result = toloka_client.find_assignments(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_assignments(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1),
        created_lt=datetime(2016, 6, 1),
        sort=['-submitted']
    )
    assert raw_result == client.unstructure(result)


def test_get_assignments(requests_mock, toloka_client, toloka_url, assignment_map):
    assignments = [dict(assignment_map, id=f'assignment-i{i}d') for i in range(50)]
    assignments.sort(key=itemgetter('id'))

    def get_assignments(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'status': ['ACCEPTED'],
            'pool_id': ['21'],
            'user_id': ['user-i1d'],
            'created_gte': ['2015-12-01T00:00:00'],
            'created_lt': ['2016-06-01T00:00:00'],
            'sort': ['id'],
        } == params

        items = [assignment for assignment in assignments if id_gt is None or assignment['id'] > id_gt][:3]
        return simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != assignments[-1]['id']})

    requests_mock.get(f'{toloka_url}/assignments', text=get_assignments)

    # Request object syntax
    request = client.search_requests.AssignmentSearchRequest(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1),
        created_lt=datetime(2016, 6, 1),
    )
    result = toloka_client.get_assignments(request)
    assert assignments == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_assignments(
        status=client.assignment.Assignment.ACCEPTED,
        pool_id='21',
        user_id='user-i1d',
        created_gte=datetime(2015, 12, 1),
        created_lt=datetime(2016, 6, 1),
    )
    assert assignments == client.unstructure(list(result))


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


def test_patch_assignment(requests_mock, toloka_client, toloka_url, assignment_map):
    raw_request = {
        'status': 'ACCEPTED',
        'public_comment': 'Well done',
    }

    raw_result = dict(assignment_map, public_comment='Well done')

    def patch_assignment(request, context):
        assert raw_request == request.json()
        return simplejson.dumps(raw_result)

    requests_mock.patch(f'{toloka_url}/assignments/assignment-i1d', text=patch_assignment)

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
def test_reward_in_get_assignment(requests_mock, toloka_client, toloka_url, assignment_map, value_to_check):
    new_assignment_map = dict(assignment_map, reward=value_to_check)
    requests_mock.get(
        f'{toloka_url}/assignments/assignment-i1d',
        text=simplejson.dumps(new_assignment_map)
    )
    result = toloka_client.get_assignment('assignment-i1d')
    assert result.reward == value_to_check
