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
def create_user_bonus_operation_running():
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
def create_user_bonus_operation_success(create_user_bonus_operation_running):
    return {**create_user_bonus_operation_running, 'status': 'SUCCESS'}


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


def test_create_user_bonus_sync_via_async(
        respx_mock, toloka_client, toloka_url,
        user_bonus_map, user_bonus_map_with_readonly,
        create_user_bonus_operation_running, create_user_bonus_operation_success, create_user_bonus_log,
):

    def user_bonus(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonus',
            'X-Low-Level-Method': 'create_user_bonus',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id='26e130ad3652443a3dc5094791e48ef9',
            async_mode='true',
        ) == request.url.params
        incoming_user_bonus = simplejson.loads(request.content)
        assert '__item_idx' in incoming_user_bonus
        incoming_user_bonus.pop('__item_idx')
        assert user_bonus_map == incoming_user_bonus
        return httpx.Response(json=create_user_bonus_operation_running, status_code=201)

    def user_bonus_op(request):
        return httpx.Response(json=create_user_bonus_operation_success, status_code=201)

    def user_bonus_log(request):
        return httpx.Response(text=simplejson.dumps(create_user_bonus_log), status_code=201)

    def return_user_bonus(request):
        return httpx.Response(text=simplejson.dumps(user_bonus_map_with_readonly), status_code=200)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonus)
    respx_mock.get(f'{toloka_url}/operations/{create_user_bonus_operation_running["id"]}').mock(side_effect=user_bonus_op)
    respx_mock.get(f'{toloka_url}/operations/{create_user_bonus_operation_running["id"]}/log').mock(side_effect=user_bonus_log)
    respx_mock.get(f'{toloka_url}/user-bonuses/user-bonus-1').mock(side_effect=return_user_bonus)

    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)

    result = toloka_client.create_user_bonus(
        user_bonus,
        operation_id='26e130ad3652443a3dc5094791e48ef9',
    )
    assert user_bonus_map_with_readonly == client.unstructure(result)


def test_create_user_bonus_sync_via_async_retry(
        respx_mock, toloka_client, toloka_url,
        user_bonus_map, user_bonus_map_with_readonly, create_user_bonus_operation_success, create_user_bonus_log
):
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
        return httpx.Response(json=create_user_bonus_operation_success, status_code=201)

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
        {'user_id': 'user-1', 'amount': Decimal('1.50')},
        {'user_id': 'user-2', 'amount': Decimal('2.00')},
    ]


@pytest.fixture
def user_bonus_map_async_with_read_only(user_bonus_map_async):
    return [{**user_bonus_map, 'id': f'user-bonus-{i + 1}'} for i, user_bonus_map in enumerate(user_bonus_map_async)]


@pytest.fixture
def create_user_bonuses_operation_id():
    return '09ee3f76-5cdc-4388-adcc-c580a3ab4c53'


@pytest.fixture
def create_user_bonuses_operation_running(create_user_bonuses_operation_id):
    return {
        'id': create_user_bonuses_operation_id,
        'type': 'USER_BONUS.BATCH_CREATE',
        'status': 'RUNNING',
        'submitted': '2020-12-13T23:32:01',
        'started': '2020-12-13T23:33:00',
        'finished': '2020-12-13T23:34:12',
        'parameters': {
            'skip_invalid_items': True,
        },
        'details': {
            'total_count': 2,
            'valid_count': 2,
            'not_valid_count': 0,
            'success_count': 0,
            'failed_count': 0,
        }
    }


@pytest.fixture
def create_user_bonuses_operation_success(create_user_bonuses_operation_running):
    return {**create_user_bonuses_operation_running, 'status': 'SUCCESS'}


@pytest.fixture
def create_user_bonuses_log(user_bonus_map_async, user_bonus_map_async_with_read_only):
    return [
        {
            'input': {
                '__item_idx': str(i),
                **user_bonus,
            },
            'output': {
                'user_bonus_id': user_bonus_map_read_only['id'],
            },
            'success': True,
            'type': 'USER_BONUS_PERSIST',
        }
        for i, (user_bonus, user_bonus_map_read_only)
        in enumerate(zip(user_bonus_map_async, user_bonus_map_async_with_read_only))
    ]


@pytest.fixture
def user_bonuses_result_map(user_bonus_map_async_with_read_only):
    return {
        'items': {
            str(i): dict(user_bonus_read_only)
            for i, user_bonus_read_only in enumerate(user_bonus_map_async_with_read_only)
        },
        'validation_errors': {},
    }


def test_create_user_bonuses_sync_via_async(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    user_bonus_map_async, create_user_bonuses_operation_id, user_bonus_map_async_with_read_only,
    create_user_bonuses_operation_running, create_user_bonuses_operation_success, create_user_bonuses_log, user_bonuses_result_map
):
    def check_user_bonuses(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'create_user_bonuses',
            'X-Low-Level-Method': 'create_user_bonuses',
        }
        check_headers(request, expected_headers)

        assert QueryParams(
            operation_id=create_user_bonuses_operation_id,
            async_mode='true',
        ) == request.url.params

        incoming_user_bonuses = []
        for ub in simplejson.loads(request.content):
            assert '__item_idx' in ub
            ub.pop('__item_idx')
            incoming_user_bonuses.append(ub)
        assert user_bonus_map_async == incoming_user_bonuses
        return httpx.Response(json=create_user_bonuses_operation_running, status_code=201)

    def user_bonuses_op(request):
        return httpx.Response(json=create_user_bonuses_operation_success, status_code=201)

    def user_bonuses_log(request):
        return httpx.Response(text=simplejson.dumps(create_user_bonuses_log), status_code=201)

    def return_user_bonuses(request):
        return httpx.Response(
            text=simplejson.dumps({'items': user_bonus_map_async_with_read_only, 'has_more': False}),
            status_code=200
        )

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=check_user_bonuses)
    respx_mock.get(f'{toloka_url}/operations/{create_user_bonuses_operation_running["id"]}').mock(side_effect=user_bonuses_op)
    respx_mock.get(f'{toloka_url}/operations/{create_user_bonuses_operation_running["id"]}/log').mock(side_effect=user_bonuses_log)
    respx_mock.get(f'{toloka_url}/user-bonuses').mock(side_effect=return_user_bonuses)

    user_bonuses = [
        client.structure(user_bonus_map, client.user_bonus.UserBonus)
        for user_bonus_map in user_bonus_map_async
    ]

    result = toloka_client.create_user_bonuses(
        user_bonuses,
        operation_id=create_user_bonuses_operation_id,
    )
    assert user_bonuses_result_map == client.unstructure(result)


def test_create_user_bonuses_sync_via_async_retry(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    user_bonus_map_async, create_user_bonuses_operation_id, user_bonus_map_async_with_read_only,
    create_user_bonuses_operation_running, create_user_bonuses_operation_success, create_user_bonuses_log, user_bonuses_result_map
):
    requests_count = 0
    first_request_op_id = None

    def check_user_bonuses(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count += 1
        if requests_count == 1:
            first_request_op_id = request.url.params['operation_id']
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == first_request_op_id
        unstructured_error = client.unstructure(IncorrectActionsApiError(
            code='OPERATION_ALREADY_EXISTS',
        ))
        del unstructured_error['status_code']

        return httpx.Response(
            json=unstructured_error,
            status_code=409
        )

    def user_bonuses_op(request):
        return httpx.Response(json=create_user_bonuses_operation_success, status_code=201)

    def user_bonuses_log(request):
        return httpx.Response(text=simplejson.dumps(create_user_bonuses_log), status_code=201)

    def return_user_bonuses(request):
        return httpx.Response(
            text=simplejson.dumps({'items': user_bonus_map_async_with_read_only, 'has_more': False}),
            status_code=200
        )

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=check_user_bonuses)
    respx_mock.get(re.compile(rf'{toloka_url}/operations/.*/log')).mock(side_effect=user_bonuses_log)
    respx_mock.get(re.compile(rf'{toloka_url}/operations/.*')).mock(side_effect=user_bonuses_op)
    respx_mock.get(f'{toloka_url}/user-bonuses').mock(side_effect=return_user_bonuses)

    user_bonuses = [
        client.structure(user_bonus_map, client.user_bonus.UserBonus)
        for user_bonus_map in user_bonus_map_async
    ]

    result = toloka_client.create_user_bonuses(user_bonuses)
    assert requests_count == 2
    assert user_bonuses_result_map == client.unstructure(result)


def test_create_user_bonuses_async(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonuses_operation_id,
    create_user_bonus_operation_running
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
        return httpx.Response(text=simplejson.dumps(create_user_bonus_operation_running), status_code=202)

    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    # Request object syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonus_map_async, List[client.UserBonus]),
        client.user_bonus.UserBonusesCreateRequestParameters(operation_id=create_user_bonuses_operation_id),
    )
    assert create_user_bonus_operation_running == client.unstructure(result)

    # Expanded syntax
    result = toloka_client.create_user_bonuses_async(
        client.structure(user_bonus_map_async, List[client.UserBonus]),
        operation_id=create_user_bonuses_operation_id,
    )
    assert create_user_bonus_operation_running == client.unstructure(result)


def test_create_user_bonuses_async_retry(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonus_operation_running
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
    ).mock(httpx.Response(json=create_user_bonus_operation_running, status_code=200))
    respx_mock.post(f'{toloka_url}/user-bonuses').mock(side_effect=user_bonuses)

    result = toloka_client.create_user_bonuses_async(client.structure(user_bonus_map_async, List[client.UserBonus]))
    assert requests_count == 2
    assert create_user_bonus_operation_running == client.unstructure(result)
