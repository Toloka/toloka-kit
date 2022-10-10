import datetime

import httpx
import simplejson
import toloka.client as client
from httpx import QueryParams

from .testutils.util_functions import check_headers


def test_find_user_restrictions(respx_mock, toloka_client, toloka_url):
    raw_result = {
        'has_more': True,
        'items': [
            {
                'id': '256',
                'scope': 'PROJECT',
                'user_id': 'user-i1d',
                'will_expire': '2019-01-01T00:00:00',
                'created': '2016-03-28T18:16:00',
                'project_id': 'p128',
            },
            {
                'id': '512',
                'scope': 'PROJECT',
                'user_id': 'user-i2d',
                'will_expire': '2019-01-01T00:00:00',
                'created': '2016-02-28T18:16:00',
                'project_id': 'p144',
            }
        ]
    }

    def user_restrictions(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_user_restrictions',
            'X-Low-Level-Method': 'find_user_restrictions',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            scope='PROJECT',
            id_gt='123',
            created_lte='2017-12-09T12:10:00',
            sort='-created,id',
            limit='50',
        ) == request.url.params
        return httpx.Response(json=raw_result, status_code=200)

    respx_mock.get(f'{toloka_url}/user-restrictions').mock(side_effect=user_restrictions)

    # Request object syntax
    request = client.search_requests.UserRestrictionSearchRequest(
        scope=client.user_restriction.UserRestriction.PROJECT,
        id_gt='123',
        created_lte=datetime.datetime(2017, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    sort = client.search_requests.UserRestrictionSortItems(['-created', 'id'])
    result = toloka_client.find_user_restrictions(request, sort=sort, limit=50)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_user_restrictions(
        scope=client.user_restriction.UserRestriction.PROJECT,
        id_gt='123',
        created_lte=datetime.datetime(2017, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
        sort=['-created', 'id'],
        limit=50,
    )
    assert raw_result == client.unstructure(result)


def test_all_find_user_restrictions(respx_mock, toloka_client, toloka_url):
    restrictions = [
        {
            'id': '256',
            'scope': 'PROJECT',
            'user_id': 'user-i1d',
            'will_expire': '2019-01-01T00:00:00',
            'created': '2016-03-28T18:16:00',
            'project_id': 'p128',
        },
        {
            'id': '512',
            'scope': 'PROJECT',
            'user_id': 'user-i2d',
            'will_expire': '2019-01-01T00:00:00',
            'created': '2016-02-28T18:16:00',
            'project_id': 'p144',
        }
    ]

    def get_user_restrictions(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_user_restrictions',
            'X-Low-Level-Method': 'find_user_restrictions',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params['id_gt']
        params = params.remove('id_gt')
        assert QueryParams(
            scope='PROJECT',
            created_lte='2017-12-09T12:10:00',
            sort='id',
        ) == params

        items = [restriction for restriction in restrictions if restriction['id'] > id_gt][:3]
        return httpx.Response(
            json={'items': items, 'has_more': items[-1]['id'] != restrictions[-1]['id']}, status_code=200
        )

    respx_mock.get(f'{toloka_url}/user-restrictions').mock(side_effect=get_user_restrictions)

    # Request object syntax
    request = client.search_requests.UserRestrictionSearchRequest(
        scope=client.user_restriction.UserRestriction.PROJECT,
        id_gt='123',
        created_lte=datetime.datetime(2017, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    result = toloka_client.get_user_restrictions(request)
    assert restrictions == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_user_restrictions(
        scope=client.user_restriction.UserRestriction.PROJECT,
        id_gt='123',
        created_lte=datetime.datetime(2017, 12, 9, 12, 10, 0, tzinfo=datetime.timezone.utc),
    )
    assert restrictions == client.unstructure(list(result))


def test_get_user_restriction(respx_mock, toloka_client, toloka_url):

    result = {
        'id': '56',
        'scope': 'ALL_PROJECTS',
        'user_id': 'user-i1d',
        'will_expire': '2019-01-01T00:00:00',
        'created': '2016-03-28T18:16:00',
    }

    def user_restrictions(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_user_restriction',
            'X-Low-Level-Method': 'get_user_restriction',
        }
        check_headers(request, expected_headers)

        return httpx.Response(json=result, status_code=200)

    respx_mock.get(f'{toloka_url}/user-restrictions/56').mock(side_effect=user_restrictions)
    assert result == client.unstructure(toloka_client.get_user_restriction('56'))


def test_set_user_restriction(respx_mock, toloka_client, toloka_url):
    user_restriction_map = {
        'scope': 'POOL',
        'user_id': 'user-i1d',
        'pool_id': '21',
        'will_expire': '2019-01-01T00:00:00',
        'private_comment': 'Too many errors',
    }
    user_restriction_map_with_readonly = {
        'id': '56',
        'created': '2016-03-28T18:16:00',
        **user_restriction_map,
    }

    def user_restrictions(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'set_user_restriction',
            'X-Low-Level-Method': 'set_user_restriction',
        }
        check_headers(request, expected_headers)

        assert user_restriction_map == simplejson.loads(request.content)
        return httpx.Response(json=user_restriction_map_with_readonly, status_code=200)

    respx_mock.put(f'{toloka_url}/user-restrictions').mock(side_effect=user_restrictions)

    # Request object syntax
    request = client.structure(
        {
            'user_id': 'user-i1d',
            'pool_id': '21',
            'private_comment': 'Too many errors',
            'will_expire': '2019-01-01T00:00:00',
        },
        client.user_restriction.PoolUserRestriction,
    )
    response = toloka_client.set_user_restriction(request)
    assert user_restriction_map_with_readonly == client.unstructure(response)


def test_delete_user_restriction(respx_mock, toloka_client, toloka_url):

    def deletion(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'delete_user_restriction',
            'X-Low-Level-Method': 'delete_user_restriction',
        }
        check_headers(request, expected_headers)
        return httpx.Response(status_code=204)

    respx_mock.delete(f'{toloka_url}/user-restrictions/user-restriction-i1d').mock(side_effect=deletion)
    toloka_client.delete_user_restriction('user-restriction-i1d')
