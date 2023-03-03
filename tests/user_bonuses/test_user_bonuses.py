import datetime
from operator import itemgetter

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams

from ..testutils.util_functions import check_headers


@pytest.mark.parametrize('value_from', [0.05, '0.05', 5])
def test_create_user_bonus_from_different_amount(value_from):
    with pytest.raises(TypeError):
        client.user_bonus.UserBonus(amount=value_from)


def test_create_user_bonus_with_none_amount():
    user_bonus = client.user_bonus.UserBonus(amount=None)
    assert user_bonus.amount is None


def test_find_user_bonuses(respx_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):
    raw_result = {'items': [user_bonus_map_with_readonly], 'has_more': False}

    def user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'find_user_bonuses',
            'X-Low-Level-Method': 'find_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            user_id='user-1',
            assignment_id='assignment-1',
            created_gte='2012-01-01T12:00:00',
            sort='created,-id',
            limit='20',
        ) == request.url.params
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=200)

    respx_mock.get(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    # Request object syntax
    request = client.search_requests.UserBonusSearchRequest(
        user_id='user-1',
        assignment_id='assignment-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    )
    sort = client.search_requests.UserBonusSortItems(['created', '-id'])
    result = toloka_client.find_user_bonuses(request, sort=sort, limit=20)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_user_bonuses(
        user_id='user-1',
        assignment_id='assignment-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        sort=['created', '-id'],
        limit=20,
    )
    assert raw_result == client.unstructure(result)


def test_get_user_bonuses(respx_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):
    user_bonuses = [dict(user_bonus_map_with_readonly, id=f'user-bonus-{i}') for i in range(50)]
    user_bonuses.sort(key=itemgetter('id'))

    def get_user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_user_bonuses',
            'X-Low-Level-Method': 'find_user_bonuses',
        }
        check_headers(request, expected_headers)

        params = request.url.params
        id_gt = params.get('id_gt', None)
        params = params.remove('id_gt')
        assert QueryParams(
            user_id='user-1',
            created_gte='2012-01-01T12:00:00',
            sort='id',
        ) == params

        items = [user_bonus for user_bonus in user_bonuses if id_gt is None or user_bonus['id'] > id_gt][:3]
        return httpx.Response(
            text=simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != user_bonuses[-1]['id']}),
            status_code=200,
        )

    respx_mock.get(f'{toloka_url}/user-bonuses').mock(side_effect=get_user_bonuses)

    # Request object syntax
    request = client.search_requests.UserBonusSearchRequest(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    )
    result = toloka_client.get_user_bonuses(request)
    assert user_bonuses == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_user_bonuses(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
    )
    assert user_bonuses == client.unstructure(list(result))


def test_get_user_bonus(respx_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):

    def user_bonus(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_user_bonus',
            'X-Low-Level-Method': 'get_user_bonus',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(user_bonus_map_with_readonly), status_code=200)

    respx_mock.get(f'{toloka_url}/user-bonuses/user-bonus-1').mock(side_effect=user_bonus)
    assert user_bonus_map_with_readonly == client.unstructure(toloka_client.get_user_bonus('user-bonus-1'))
