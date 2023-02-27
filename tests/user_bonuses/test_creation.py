import re
from decimal import Decimal
from typing import List

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client.exceptions import IncorrectActionsApiError

from ..testutils.util_functions import check_headers


@pytest.mark.parametrize('value_from', [0.05, '0.05', 5])
def test_create_user_bonus_from_different_amount(value_from):
    with pytest.raises(TypeError):
        client.user_bonus.UserBonus(amount=value_from)


def test_create_user_bonus_with_none_amount():
    user_bonus = client.user_bonus.UserBonus(amount=None)
    assert user_bonus.amount is None


def test_create_user_bonus_sync(respx_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly):

    def user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonus',
            'X-Low-Level-Method': 'create_user_bonus',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id=request.url.params['operation_id'],
            async_mode='false',
        ) == request.url.params
        assert user_bonus_map == simplejson.loads(request.content, parse_float=Decimal)
        return httpx.Response(text=simplejson.dumps(user_bonus_map_with_readonly), status_code=201)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)
    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)
    assert user_bonus.amount == Decimal('1.50')
    result = toloka_client.create_user_bonus(
        user_bonus,
        client.user_bonus.UserBonusesCreateRequestParameters(async_mode=False),
    )
    assert user_bonus_map_with_readonly == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonus(user_bonus, async_mode=False)
    assert user_bonus_map_with_readonly == client.unstructure(result)


def test_create_user_bonuses_sync(respx_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly):
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

    def user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonuses',
            'X-Low-Level-Method': 'create_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id=request.url.params['operation_id'],
            skip_invalid_items='true',
            async_mode='false',
        ) == request.url.params
        assert [{'user_id': 'user-2', 'amount': -5}, user_bonus_map] == simplejson.loads(request.content, parse_float=Decimal)
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=201)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)


    user_bonuses_to_create = [
        client.user_bonus.UserBonus(user_id='user-2', amount=Decimal('-5.')),
        client.structure(user_bonus_map, client.user_bonus.UserBonus),
    ]
    # Request object syntax
    result = toloka_client.create_user_bonuses(
        user_bonuses_to_create,
        client.user_bonus.UserBonusesCreateRequestParameters(skip_invalid_items=True, async_mode=False),
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses(
        user_bonuses_to_create,
        skip_invalid_items=True,
        async_mode=False,
    )
    assert raw_result == client.unstructure(result)


@pytest.fixture
def create_user_bonus_operation():
    return {
        'id': '26e130ad3652443a3dc5094791e48ef9',
        'type': 'USER_BONUS.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2020-12-13T23:32:01',
        'started': '2020-12-13T23:33:00',
        'finished': '2020-12-13T23:34:12',
        'parameters': {
            'skip_invalid_items': True
        },
        'details': {
            'total_count': 1,
            'valid_count': 1,
            'not_valid_count': 0,
            'success_count': 1,
            'failed_count': 0,
        }
    }


@pytest.fixture
def create_user_bonus_log():
    return [
        {
            'input': {
                '__item_idx': '0',
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
            },
            'output': {
                'user_bonus_id': 'user-bonus-1',
            },
            'success': True,
            'type': 'USER_BONUS_PERSIST',
        },
    ]


def test_create_user_bonus_retry(respx_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly,
                                 create_user_bonus_operation, create_user_bonus_log):
    requests_count = 0
    first_request_op_id = '26e130ad3652443a3dc5094791e48ef9'

    def user_bonuses(request):
        nonlocal requests_count

        requests_count += 1
        if requests_count == 1:
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == first_request_op_id
        unstructured_error = client.unstructure(
            IncorrectActionsApiError(
                code='OPERATION_ALREADY_EXISTS',
            )
        )
        del unstructured_error['status_code']

        return httpx.Response(
            json=unstructured_error,
            status_code=409
        )

    def user_bonus_op(request):
        return httpx.Response(json=create_user_bonus_operation, status_code=201)

    def user_bonus_log(request):
        return httpx.Response(text=simplejson.dumps(create_user_bonus_log), status_code=201)

    def user_bonus(request):
        return httpx.Response(text=simplejson.dumps(user_bonus_map_with_readonly), status_code=200)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    respx_mock.get(f'{toloka_url}/operations/{first_request_op_id}').mock(side_effect=user_bonus_op)
    respx_mock.get(f'{toloka_url}/operations/{first_request_op_id}/log').mock(side_effect=user_bonus_log)

    respx_mock.get(f'{toloka_url}/user-bonuses/user-bonus-1').mock(side_effect=user_bonus)

    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)

    result = toloka_client.create_user_bonus(user_bonus, operation_id=first_request_op_id)
    assert user_bonus_map_with_readonly == client.unstructure(result)


def test_create_user_bonuses_without_message(
    respx_mock, toloka_client, toloka_url,
    user_bonus_map_without_message, user_bonus_map_without_message_with_readonly
):
    raw_result = {'items': {'0': user_bonus_map_without_message_with_readonly}}

    def user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonuses',
            'X-Low-Level-Method': 'create_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id=request.url.params['operation_id'],
            skip_invalid_items='true',
            async_mode='false',
        ) == request.url.params
        assert [user_bonus_map_without_message] == simplejson.loads(request.content, parse_float=Decimal)
        return httpx.Response(text=simplejson.dumps(raw_result), status_code=201)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    # Request object syntax
    result = toloka_client.create_user_bonuses(
        [client.structure(user_bonus_map_without_message, client.user_bonus.UserBonus)],
        client.user_bonus.UserBonusesCreateRequestParameters(skip_invalid_items=True, async_mode=False),
    )
    assert raw_result == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses(
        [client.structure(user_bonus_map_without_message, client.user_bonus.UserBonus)],
        skip_invalid_items=True,
        async_mode=False,
    )
    assert raw_result == client.unstructure(result)


@pytest.fixture
def user_bonus_map_async():
    return [
        {'user_id': 'user-1', 'amount': Decimal('10.00')},
        {'user_id': 'user-2', 'amount': Decimal('12.00')},
    ]


@pytest.fixture
def create_user_bonuses_operation_id():
    return '09ee3f76-5cdc-4388-adcc-c580a3ab4c53'


@pytest.fixture
def create_user_bonuses_operation_map(create_user_bonuses_operation_id):
    return {
        'id': create_user_bonuses_operation_id,
        'type': 'USER_BONUS.BATCH_CREATE',
        'status': 'SUCCESS',
        'submitted': '2016-10-23T14:02:01',
        'started': '2016-10-23T14:02:02',
        'finished': '2016-10-23T14:02:03',
    }


def test_create_user_bonuses_async(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonuses_operation_id,
    create_user_bonuses_operation_map
):

    def user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonuses_async',
            'X-Low-Level-Method': 'create_user_bonuses_async',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            async_mode='true',
            operation_id=create_user_bonuses_operation_id,
        ) == request.url.params
        assert simplejson.dumps(user_bonus_map_async) == request.content.decode('utf8')
        return httpx.Response(text=simplejson.dumps(create_user_bonuses_operation_map), status_code=202)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    # Request object syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonus_map_async, List[client.UserBonus]),
        client.user_bonus.UserBonusesCreateRequestParameters(operation_id=create_user_bonuses_operation_id),
    )
    assert create_user_bonuses_operation_map == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonus_map_async, List[client.UserBonus]),
        operation_id=create_user_bonuses_operation_id,
    )
    assert create_user_bonuses_operation_map == client.unstructure(result)


def test_create_user_bonuses_async_retry(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonuses_operation_map
):
    requests_count = 0
    first_request_op_id = None

    def user_bonuses(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count += 1
        if requests_count == 1:
            first_request_op_id = request.url.params['operation_id']
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == first_request_op_id
        unstructured_error = client.unstructure(
            IncorrectActionsApiError(
                code='OPERATION_ALREADY_EXISTS',
            )
        )
        del unstructured_error['status_code']

        return httpx.Response(
            json=unstructured_error,
            status_code=409
        )

    respx_mock.get(
        re.compile(rf'{toloka_url}/operations/.*')
    ).mock(httpx.Response(json=create_user_bonuses_operation_map, status_code=200))
    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    result = toloka_client.create_user_bonuses_async(client.structure(user_bonus_map_async, List[client.UserBonus]))
    assert requests_count == 2
    assert create_user_bonuses_operation_map == client.unstructure(result)
