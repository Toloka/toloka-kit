import datetime
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client


@pytest.fixture
def set_user_skill_map():
    return {
        'skill_id': 'skill-i1d',
        'user_id': 'user-i1d',
        'value': 85.42,
    }


@pytest.fixture
def user_skill_map():
    return {
        'skill_id': 'skill-i1d',
        'user_id': 'user-i1d',
        'value': 85,
        'exact_value': 85.42,
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
        assert {
            'skill_id': ['skill-i1d'],
            'created_gt': ['2016-03-25T00:00:00'],
            'modified_lt': ['2017-03-25T00:00:00'],
            'sort': ['id'],
            'limit': ['100'],
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(f'{toloka_url}/user-skills', json=user_skills, status_code=200)

    # Request object syntax
    request = client.search_requests.UserSkillSearchRequest(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25),
        modified_lt=datetime.datetime(2017, 3, 25),
    )
    sort = client.search_requests.UserSkillSortItems(['id'])
    result = toloka_client.find_user_skills(request, sort=sort, limit=100)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_user_skills(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25),
        modified_lt=datetime.datetime(2017, 3, 25),
        sort=['id'],
        limit=100,
    )
    assert raw_result == client.unstructure(result)


def test_get_user_skills(requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly):
    user_skills = [dict(user_skill_map_with_readonly, id=f'user-skill-i{i}d') for i in range(50)]
    user_skills.sort(key=itemgetter('id'))

    def get_user_skills(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'skill_id': ['skill-i1d'],
            'created_gt': ['2016-03-25T00:00:00'],
            'modified_lt': ['2017-03-25T00:00:00'],
            'sort': ['id'],
        } == params

        items = [user_skill for user_skill in user_skills if id_gt is None or user_skill['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != user_skills[-1]['id']}

    requests_mock.get(f'{toloka_url}/user-skills', json=get_user_skills, status_code=200)

    # Request object syntax
    request = client.search_requests.UserSkillSearchRequest(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25),
        modified_lt=datetime.datetime(2017, 3, 25),
    )
    result = toloka_client.get_user_skills(request)
    assert user_skills == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_user_skills(
        skill_id='skill-i1d',
        created_gt=datetime.datetime(2016, 3, 25),
        modified_lt=datetime.datetime(2017, 3, 25),
    )
    assert user_skills == client.unstructure(list(result))


def test_get_user_skill(requests_mock, toloka_client, toloka_url, user_skill_map_with_readonly):

    requests_mock.get(
        f'{toloka_url}/user-skills/user-skill-i1d',
        json=user_skill_map_with_readonly,
        status_code=200
    )

    assert user_skill_map_with_readonly == client.unstructure(toloka_client.get_user_skill('user-skill-i1d'))


def test_set_user_skill(requests_mock, toloka_client, toloka_url, set_user_skill_map, user_skill_map_with_readonly):

    def user_skills(request, context):
        assert set_user_skill_map == request.json()
        return user_skill_map_with_readonly

    requests_mock.put(f'{toloka_url}/user-skills', json=user_skills, status_code=201)

    # Request object syntax
    request = client.structure(
        {
            'skill_id': 'skill-i1d',
            'user_id': 'user-i1d',
            'value': 85.42,
        },
        client.user_skill.SetUserSkillRequest
    )
    response = toloka_client.set_user_skill(request)
    assert user_skill_map_with_readonly == client.unstructure(response)

    # Expanded syntax
    response = toloka_client.set_user_skill(skill_id='skill-i1d', user_id='user-i1d', value=85.42)
    assert user_skill_map_with_readonly == client.unstructure(response)


def test_delete_user_skill(requests_mock, toloka_client, toloka_url):
    requests_mock.delete(f'{toloka_url}/user-skills/user-skill-i1d', status_code=204)
    toloka_client.delete_user_skill('user-skill-i1d')
