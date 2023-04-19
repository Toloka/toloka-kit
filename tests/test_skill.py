import httpx
import simplejson
from httpx import QueryParams
import logging
from operator import itemgetter
from urllib.parse import urlparse, parse_qs

import pytest
import toloka.client as client

from .testutils.util_functions import check_headers


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
    return {
        **skill_header,
        'id': '21',
        'created': '2015-12-16T12:55:01',
        'owner': {
            'id': 'c3a50f44cd3e1b8202465569ced289eb',
            'myself': True,
        },
    }


def test_find_skills(skill_sample, respx_mock, toloka_client, toloka_url):
    raw_result = {'items': [skill_sample], 'has_more': False}

    def find_skill(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_skills',
            'X-Low-Level-Method': 'find_skills',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            id_gt='20',
            sort='-created,id',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/skills').mock(side_effect=find_skill)

    # Request object syntax
    request = client.search_requests.SkillSearchRequest(id_gt='20')
    sort = client.search_requests.SkillSortItems(['-created', 'id'])

    result = toloka_client.find_skills(request, sort=sort)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_skills(id_gt='20', sort=['-created', 'id'])
    assert raw_result == client.unstructure(result)


def test_get_skills(skill_sample, respx_mock, toloka_client, toloka_url):
    skills = [dict(skill_sample, id=str(i)) for i in range(50)]
    skills.sort(key=itemgetter('id'))
    expected_skills = [skill for skill in skills if skill['id'] > '20']

    def get_skill(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_skills',
            'X-Low-Level-Method': 'find_skills',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(sort='id') == params

        items = [skill for skill in skills if id_gt if skill['id'] > id_gt][:3]
        return httpx.Response(json={'items': items, 'has_more': items[-1]['id'] != skills[-1]['id']}, status_code=200)

    respx_mock.get(f'{toloka_url}/skills').mock(side_effect=get_skill)

    # Request object syntax
    request = client.search_requests.SkillSearchRequest(id_gt='20')
    result = toloka_client.get_skills(request)
    assert expected_skills == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_skills(id_gt='20')
    assert expected_skills == client.unstructure(list(result))


def test_get_skill(skill_sample, respx_mock, toloka_client, toloka_url):

    def skill(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_skill',
            'X-Low-Level-Method': 'get_skill',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=skill_sample, status_code=200)

    respx_mock.get(f'{toloka_url}/skills/21').mock(side_effect=skill)

    result = toloka_client.get_skill('21')
    assert skill_sample == client.unstructure(result)


def test_create_skill(skill_sample, skill_header, respx_mock, toloka_client, toloka_url, caplog):
    def create_skill(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_skill',
            'X-Low-Level-Method': 'create_skill',
        }
        check_headers(request, expected_headers)

        assert simplejson.loads(request.content) == skill_header
        return httpx.Response(json=skill_sample, status_code=201)

    respx_mock.post(f'{toloka_url}/skills').mock(side_effect=create_skill)

    # Request object syntax
    with caplog.at_level(logging.INFO):
        caplog.clear()
        result = toloka_client.create_skill(client.Skill(**skill_header))
        assert [log for log in caplog.record_tuples if log[0] == 'toloka.client'] == [(
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


def test_update_skill(skill_sample, skill_header, respx_mock, toloka_client, toloka_url):
    def update_skill(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'update_skill',
            'X-Low-Level-Method': 'update_skill',
        }
        check_headers(request, expected_headers)

        assert simplejson.loads(request.content) == skill_header
        return httpx.Response(json=skill_sample, status_code=200)

    respx_mock.put(f'{toloka_url}/skills/21').mock(side_effect=update_skill)

    result = toloka_client.update_skill(
        '21', client.Skill(**skill_header)
    )
    assert skill_sample == client.unstructure(result)
