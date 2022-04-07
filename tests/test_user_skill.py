import datetime
from decimal import Decimal
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import pytest
import simplejson
import toloka.client as client

from .testutils.util_functions import check_headers


@pytest.fixture
def set_user_skill_map():
    return {
        'skill_id': 'skill-i1d',
        'user_id': 'user-i1d',
        'value': Decimal('85.42'),
    }


@pytest.fixture
def user_skill_map():
    return {
        'skill_id': 'skill-i1d',
        'user_id': 'user-i1d',
        'value': 85,
        'exact_value': Decimal('85.42'),
    }


@pytest.fixture
def user_skill_map_with_readonly(user_skill_map):
    return dict(
        user_skill_map,
        id='user-skill-i1d',
        created='2016-03-25T15:59:08',
        modified='2017-03-24T15:59:08',
    )


def test_find_user_skills(requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly):
    raw_result = {'items': [user_skill_map_with_readonly], 'has_more': True}

    def user_skills(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_user_skills',
            'X-Low-Level-Method': 'find_user_skills',
        }
        check_headers(request, expected_headers)

        assert {
            'skill_id': ['skill-i1d'],
            'created_gt': ['2016-03-25T00:00:00'],
            'modified_lt': ['2017-03-25T00:00:00'],
            'sort': ['id'],
            'limit': ['100'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_url}/user-skills', text=user_skills, status_code=200)

    # Request object syntax
    request = client.search_requests.UserSkillSearchRequest(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25, tzinfo=datetime.timezone.utc),
        modified_lt=datetime.datetime(2017, 3, 25, tzinfo=datetime.timezone.utc),
    )
    sort = client.search_requests.UserSkillSortItems(['id'])
    result = toloka_client.find_user_skills(request, sort=sort, limit=100)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_user_skills(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25, tzinfo=datetime.timezone.utc),
        modified_lt=datetime.datetime(2017, 3, 25, tzinfo=datetime.timezone.utc),
        sort=['id'],
        limit=100,
    )
    assert raw_result == client.unstructure(result)


def test_get_user_skills(requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly):
    user_skills = [dict(user_skill_map_with_readonly, id=f'user-skill-i{i}d') for i in range(50)]
    user_skills.sort(key=itemgetter('id'))

    def get_user_skills(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_user_skills',
            'X-Low-Level-Method': 'find_user_skills',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'skill_id': ['skill-i1d'],
            'created_gt': ['2016-03-25T00:00:00'],
            'modified_lt': ['2017-03-25T00:00:00'],
            'sort': ['id'],
        } == params

        items = [user_skill for user_skill in user_skills if id_gt is None or user_skill['id'] > id_gt][:3]
        return simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != user_skills[-1]['id']})

    requests_mock.get(f'{toloka_url}/user-skills', text=get_user_skills, status_code=200)

    # Request object syntax
    request = client.search_requests.UserSkillSearchRequest(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25, tzinfo=datetime.timezone.utc),
        modified_lt=datetime.datetime(2017, 3, 25, tzinfo=datetime.timezone.utc),
    )
    result = toloka_client.get_user_skills(request)
    assert user_skills == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_user_skills(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25, tzinfo=datetime.timezone.utc),
        modified_lt=datetime.datetime(2017, 3, 25, tzinfo=datetime.timezone.utc),
    )
    assert user_skills == client.unstructure(list(result))


def test_get_user_skill(requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly):

    def user_skill(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_user_skill',
            'X-Low-Level-Method': 'get_user_skill',
        }
        check_headers(request, expected_headers)

        return simplejson.dumps(user_skill_map_with_readonly)

    requests_mock.get(
        f'{toloka_url}/user-skills/user-skill-i1d',
        text=user_skill,
        status_code=200
    )

    assert user_skill_map_with_readonly == client.unstructure(toloka_client.get_user_skill('user-skill-i1d'))


def test_set_user_skill(requests_mock, toloka_client, toloka_url, set_user_skill_map, user_skill_map_with_readonly):

    user_skill_request_map = {
        'skill_id': 'skill-i1d',
        'user_id': 'user-i1d',
        'value': Decimal('85.42'),
    }

    def user_skills(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'set_user_skill',
            'X-Low-Level-Method': 'set_user_skill',
        }
        check_headers(request, expected_headers)

        assert request.text == simplejson.dumps(user_skill_request_map)
        assert set_user_skill_map == request.json(parse_float=Decimal)
        return simplejson.dumps(user_skill_map_with_readonly)

    requests_mock.put(f'{toloka_url}/user-skills', text=user_skills, status_code=201)

    # Request object syntax
    request = client.structure(user_skill_request_map, client.user_skill.SetUserSkillRequest)
    assert request.value == Decimal('85.42')
    response = toloka_client.set_user_skill(request)
    assert user_skill_map_with_readonly == client.unstructure(response)

    # Expanded syntax
    response = toloka_client.set_user_skill(skill_id='skill-i1d', user_id='user-i1d', value=Decimal('85.42'))
    assert user_skill_map_with_readonly == client.unstructure(response)


def test_delete_user_skill(requests_mock, toloka_client, toloka_url):

    def user_skills(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'delete_user_skill',
            'X-Low-Level-Method': 'delete_user_skill',
        }
        check_headers(request, expected_headers)

    requests_mock.delete(f'{toloka_url}/user-skills/user-skill-i1d', status_code=204, text=user_skills)
    toloka_client.delete_user_skill('user-skill-i1d')


@pytest.mark.parametrize('value_from', [0.05, '0.05', 5])
def test_create_set_user_skill_from_different_value(value_from):
    with pytest.raises(TypeError):
        client.user_skill.SetUserSkillRequest(value=value_from)


def test_create_set_user_skill_with_none_value():
    set_user_skill = client.user_skill.SetUserSkillRequest(value=None)
    assert set_user_skill.value is None


@pytest.mark.parametrize('value_to_check', [Decimal('0.05'), Decimal('0.0005')])
def test_exact_value_in_user_skill(
    requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly,
    value_to_check
):
    new_map = dict(user_skill_map_with_readonly, exact_value=value_to_check)

    def new_user_skills(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_user_skill',
            'X-Low-Level-Method': 'get_user_skill',
        }
        check_headers(request, expected_headers)

        return simplejson.dumps(new_map)

    requests_mock.get(
        f'{toloka_url}/user-skills/user-skill-i1d',
        text=new_user_skills,
        status_code=200
    )
    user_skill = toloka_client.get_user_skill('user-skill-i1d')
    assert user_skill.exact_value == value_to_check
