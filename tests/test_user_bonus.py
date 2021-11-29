import datetime
from decimal import Decimal
from operator import itemgetter
from typing import List
from urllib.parse import urlparse, parse_qs

import pytest
import simplejson
import toloka.client as client

from .testutils.util_functions import check_headers


@pytest.fixture
def user_bonus_map():
    return {
        'user_id': 'user-1',
        'amount': Decimal('1.50'),
        'private_comment': 'pool_23214',
        'assignment_id': 'assignment-1',
        'public_title': {
            'EN': 'Good Job!',
            'RU': 'Молодец!',
        },
        'public_message': {
            'EN': 'Ten tasks completed',
            'RU': 'Выполнено 10 заданий',
        }
    }


@pytest.fixture
def user_bonus_map_without_message(user_bonus_map):
    user_bonus_map_without_message = user_bonus_map.copy()
    del user_bonus_map_without_message['public_title']
    del user_bonus_map_without_message['public_message']
    user_bonus_map_without_message['without_message'] = True
    return user_bonus_map_without_message


@pytest.fixture
def user_bonus_map_with_readonly(user_bonus_map):
    return dict(
        user_bonus_map,
        id='user-bonus-1',
        created='2016-10-23T13:27:00',
    )


@pytest.fixture
def user_bonus_map_without_message_with_readonly(user_bonus_map_without_message):
    return dict(
        user_bonus_map_without_message,
        id='user-bonus-1',
        created='2016-10-23T13:27:00',
    )


def test_create_user_bonus(requests_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly):

    def user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_user_bonus',
            'X-Low-Level-Method': 'create_user_bonus',
        }
        check_headers(request, expected_headers)

        assert {'skip_invalid_items': ['true']} == parse_qs(urlparse(request.url).query)
        assert user_bonus_map == request.json()
        return simplejson.dumps(user_bonus_map_with_readonly)

    requests_mock.post(f'{toloka_url}/user-bonuses', text=user_bonuses, status_code=201)
    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)
    assert user_bonus.amount == Decimal('1.50')
    result = toloka_client.create_user_bonus(
        user_bonus,
        client.user_bonus.UserBonusCreateRequestParameters(skip_invalid_items=True),
    )
    assert user_bonus_map_with_readonly == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonus(user_bonus, skip_invalid_items=True)
    assert user_bonus_map_with_readonly == client.unstructure(result)


def test_create_user_bonuses(requests_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly):
    raw_result = {
        'items': {'1': user_bonus_map_with_readonly},
        'validation_errors': {
            '0': {
                'amount': {
                    'code': 'VALUE_LESS_THAN_MIN',
                    'message': 'Value must be greater or equal to 0.01',
                    'params': [Decimal('0.01')],
                }
            }
        }
    }

    def user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_user_bonuses',
            'X-Low-Level-Method': 'create_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert {'skip_invalid_items': ['true']} == parse_qs(urlparse(request.url).query)
        assert [{'user_id': 'user-2', 'amount': -5}, user_bonus_map] == request.json()
        return simplejson.dumps(raw_result)

    requests_mock.post(f'{toloka_url}/user-bonuses', text=user_bonuses, status_code=201)

    # Request object syntax
    result = toloka_client.create_user_bonuses(
        [
            client.user_bonus.UserBonus(user_id='user-2', amount=Decimal('-5.')),
            client.structure(user_bonus_map, client.user_bonus.UserBonus),
        ],
        client.user_bonus.UserBonusCreateRequestParameters(skip_invalid_items=True),
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses(
        [
            client.user_bonus.UserBonus(user_id='user-2', amount=Decimal('-5.')),
            client.structure(user_bonus_map, client.user_bonus.UserBonus),
        ],
        skip_invalid_items=True,
    )
    assert raw_result == client.unstructure(result)


def test_create_user_bonuses_without_message(
    requests_mock, toloka_client, toloka_url,
    user_bonus_map_without_message, user_bonus_map_without_message_with_readonly
):
    raw_result = {'items': {'0': user_bonus_map_without_message_with_readonly}}

    def user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_user_bonuses',
            'X-Low-Level-Method': 'create_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert {'skip_invalid_items': ['true']} == parse_qs(urlparse(request.url).query)
        assert [user_bonus_map_without_message] == request.json()
        return simplejson.dumps(raw_result)

    requests_mock.post(f'{toloka_url}/user-bonuses', text=user_bonuses, status_code=201)

    # Request object syntax
    result = toloka_client.create_user_bonuses(
        [client.structure(user_bonus_map_without_message, client.user_bonus.UserBonus)],
        client.user_bonus.UserBonusCreateRequestParameters(skip_invalid_items=True),
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses(
        [client.structure(user_bonus_map_without_message, client.user_bonus.UserBonus)],
        skip_invalid_items=True,
    )
    assert raw_result == client.unstructure(result)


def test_create_user_bonuses_async(requests_mock, toloka_client, toloka_url):

    user_bonuses_map = [
        {'user_id': 'user-1', 'amount': Decimal('10.00')},
        {'user_id': 'user-2', 'amount': Decimal('12.00')},
    ]

    operation_id = '09ee3f76-5cdc-4388-adcc-c580a3ab4c53'

    raw_result = {
        'id': operation_id,
        'type': 'USER_BONUS.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2016-10-23T14:02:01',
        'started': '2016-10-23T14:02:02',
        'finished': '2016-10-23T14:02:03',
    }

    def user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'create_user_bonuses_async',
            'X-Low-Level-Method': 'create_user_bonuses_async',
        }
        check_headers(request, expected_headers)

        assert {
            'async_mode': ['true'],
            'operation_id': [operation_id],
        } == parse_qs(urlparse(request.url).query)
        assert simplejson.dumps(user_bonuses_map) == request.text
        return simplejson.dumps(raw_result)

    requests_mock.post(f'{toloka_url}/user-bonuses', text=user_bonuses, status_code=202)

    # Request object syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonuses_map, List[client.UserBonus]),
        client.UserBonusCreateRequestParameters(operation_id=operation_id)
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonuses_map, List[client.UserBonus]),
        operation_id=operation_id
    )
    assert raw_result == client.unstructure(result)


def test_find_user_bonuses(requests_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):
    raw_result = {'items': [user_bonus_map_with_readonly], 'has_more': False}

    def user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'find_user_bonuses',
            'X-Low-Level-Method': 'find_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert {
            'user_id': ['user-1'],
            'created_gte': ['2012-01-01T12:00:00'],
            'sort': ['created,-id'],
            'limit': ['20'],
        } == parse_qs(urlparse(request.url).query)
        return simplejson.dumps(raw_result)

    requests_mock.get(f'{toloka_url}/user-bonuses', text=user_bonuses)

    # Request object syntax
    request = client.search_requests.UserBonusSearchRequest(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0)
    )
    sort = client.search_requests.UserBonusSortItems(['created', '-id'])
    result = toloka_client.find_user_bonuses(request, sort=sort, limit=20)
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.find_user_bonuses(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0),
        sort=['created', '-id'],
        limit=20,
    )
    assert raw_result == client.unstructure(result)


def test_get_user_bonuses(requests_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):
    user_bonuses = [dict(user_bonus_map_with_readonly, id=f'user-bonus-{i}') for i in range(50)]
    user_bonuses.sort(key=itemgetter('id'))

    def get_user_bonuses(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_user_bonuses',
            'X-Low-Level-Method': 'find_user_bonuses',
        }
        check_headers(request, expected_headers)

        params = parse_qs(urlparse(request.url).query)
        id_gt = params.pop('id_gt')[0] if 'id_gt' in params else None
        assert {
            'user_id': ['user-1'],
            'created_gte': ['2012-01-01T12:00:00'],
            'sort': ['id'],
        } == params

        items = [user_bonus for user_bonus in user_bonuses if id_gt is None or user_bonus['id'] > id_gt][:3]
        return simplejson.dumps({'items': items, 'has_more': items[-1]['id'] != user_bonuses[-1]['id']})

    requests_mock.get(f'{toloka_url}/user-bonuses', text=get_user_bonuses)

    # Request object syntax
    request = client.search_requests.UserBonusSearchRequest(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0)
    )
    result = toloka_client.get_user_bonuses(request)
    assert user_bonuses == client.unstructure(list(result))

    # Expanded syntax
    result = toloka_client.get_user_bonuses(
        user_id='user-1',
        created_gte=datetime.datetime(2012, 1, 1, 12, 0, 0),
    )
    assert user_bonuses == client.unstructure(list(result))


def test_get_user_bonus(requests_mock, toloka_client, toloka_url, user_bonus_map_with_readonly):

    def user_bonus(request, context):
        expected_headers = {
            'X-Caller-Context': 'client',
            'X-Top-Level-Method': 'get_user_bonus',
            'X-Low-Level-Method': 'get_user_bonus',
        }
        check_headers(request, expected_headers)

        return simplejson.dumps(user_bonus_map_with_readonly)

    requests_mock.get(f'{toloka_url}/user-bonuses/user-bonus-1', text=user_bonus)
    assert user_bonus_map_with_readonly == client.unstructure(toloka_client.get_user_bonus('user-bonus-1'))


@pytest.mark.parametrize('value_from', [0.05, '0.05', 5])
def test_create_user_bonus_from_different_amount(value_from):
    with pytest.raises(TypeError):
        client.user_bonus.UserBonus(amount=value_from)


def test_create_user_bonus_with_none_amount():
    user_bonus = client.user_bonus.UserBonus(amount=None)
    assert user_bonus.amount is None
