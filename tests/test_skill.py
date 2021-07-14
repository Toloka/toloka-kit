import logging
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client


@pytest.fixture
def skill_header():
    return {
        'name': 'Skill name',
        'private_comment': 'Private comment',
        'hidden': False,
        'public_requester_description': {
            'EN': 'Skill description',
            'RU': 'Описание навыка',
        },
    }


@pytest.fixture
def skill_sample(skill_header):
    return dict(skill_header, id='21', created='2015-12-16T12:55:01')


def test_find_skills(skill_sample, requests_mock, toloka_client, toloka_url):
    raw_result = {'items': [skill_sample], 'has_more': False}

    def find_skill(request, context):
        assert {
            'id_gt': ['20'],
            'sort': ['-created,id']
        } == parse_qs(urlparse(request.url).query)
        return raw_result

    requests_mock.get(
        f'{toloka_url}/skills',
        json=find_skill,
        status_code=200
    )

    # Request object syntax
    request = client.search_requests.SkillSearchRequest(id_gt=20)
    sort = client.search_requests.SkillSortItems(['-created', 'id'])

    result = toloka_client.find_skills(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_skills(id_gt=20, sort=['-created', 'id'])
    assert raw_result == client.unstructure(result)


def test_get_skills(skill_sample, requests_mock, toloka_client, toloka_url):
    skills = [dict(skill_sample, id=str(i)) for i in range(50)]
    skills.sort(key=itemgetter('id'))
    expected_skills = [skill for skill in skills if skill['id'] > '20']

    def get_skill(request, context):
        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0]
        assert {'sort': ['id']} == params

        items = [skill for skill in skills if id_gt if skill['id'] > id_gt][:3]
        return {'items': items, 'has_more': items[-1]['id'] != skills[-1]['id']}

    requests_mock.get(
        f'{toloka_url}/skills',
        json=get_skill,
        status_code=200
    )

    # Request object syntax
    request = client.search_requests.SkillSearchRequest(id_gt=20)
    result = toloka_client.get_skills(request)
    assert expected_skills == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_skills(id_gt=20)
    assert expected_skills == client.unstructure(list(result))


def test_get_skill(skill_sample, requests_mock, toloka_client, toloka_url):
    requests_mock.get(
        f'{toloka_url}/skills/21',
        json=skill_sample,
        status_code=200
    )

    result = toloka_client.get_skill('21')
    assert skill_sample == client.unstructure(result)


def test_create_skill(skill_sample, skill_header, requests_mock, toloka_client, toloka_url, caplog):
    def create_skill(request, context):
        assert request.json() == skill_header
        return skill_sample

    requests_mock.post(
        f'{toloka_url}/skills',
        json=create_skill,
        status_code=201
    )

    # Request object syntax
    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.create_skill(client.Skill(**skill_header))
        assert caplog.record_tuples == [(
            'toloka.client',
            logging.INFO,
            'A new skill with ID "21" has been created. Link to open in web interface: https://sandbox.toloka.yandex.com/requester/quality/skill/21'
        )]
        assert skill_sample == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_skill(
        name='Skill name',
        private_comment='Private comment',
        hidden=False,
        public_requester_description={
            'EN': 'Skill description',
            'RU': 'Описание навыка',
        },
    )
    assert skill_sample == client.unstructure(result)


def test_create_skill_readonly_fields(skill_sample, toloka_client):
    with pytest.raises(TypeError):
        toloka_client.create_skill(
            id='21',
            name='Skill name',
            private_comment='Private comment',
            hidden=False,
            public_requester_description={
                'EN': 'Skill description',
                'RU': 'Описание навыка',
            },
        )


def test_update_skill(skill_sample, skill_header, requests_mock, toloka_client, toloka_url):
    def update_skill(request, context):
        assert request.json() == skill_header
        return skill_sample

    requests_mock.put(
        f'{toloka_url}/skills/21',
        json=update_skill,
        status_code=200
    )

    result = toloka_client.update_skill(
        '21', client.Skill(**skill_header)
    )
    assert skill_sample == client.unstructure(result)
