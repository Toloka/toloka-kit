import re
from decimal import Decimal
from typing import List
from uuid import UUID

import httpx
import pytest
import simplejson
import toloka.client as client
from httpx import QueryParams
from toloka.client import UserBonus
from toloka.client.batch_create_results import UserBonusBatchCreateResult
from toloka.client.exceptions import FailedOperation, IncorrectActionsApiError
from toloka.client.operations import Operation

from ..testutils.util_functions import (
    assert_async_object_creation_is_successful, assert_retried_async_object_creation_returns_existing_operation,
    assert_retried_failed_operation_fails_with_failed_operation_exception,
    assert_retried_sync_via_async_object_creation_returns_already_existing_object,
    assert_sync_via_async_object_creation_is_successful, check_headers,
)


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
        assert [{'user_id': 'user-2', 'amount': -5}, user_bonus_map] == simplejson.loads(
            request.content, parse_float=Decimal
        )
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
def operation_id() -> UUID:
    return UUID('26e130ad-3652-443a-3dc5-094791e48ef9')


@pytest.fixture
def create_user_bonus_operation_running(operation_id):
    return {
        'id': str(operation_id),
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
def create_user_bonus_operation_fail(create_user_bonus_operation_running):
    return {**create_user_bonus_operation_running, 'status': 'FAIL'}


@pytest.fixture
def create_user_bonus_log():
    return [
        {
            'input': {
                '__item_idx': '0',
                'user_id': 'user-1',
                'amount': '1.50',
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
    operation_id
):
    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)

    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonus,
        create_method_kwargs={'user_bonus': user_bonus, 'operation_id': operation_id},
        returned_object=simplejson.dumps(user_bonus_map_with_readonly),
        expected_response_object=UserBonus.structure(user_bonus_map_with_readonly),
        operation_log=simplejson.dumps(create_user_bonus_log),
        create_object_path='user-bonuses',
        get_object_path='user-bonuses/user-bonus-1',
        operation_running=Operation.structure(create_user_bonus_operation_running),
        success_operation=Operation.structure(create_user_bonus_operation_success),
        expected_query_params={
            'operation_id': str(operation_id),
            'async_mode': 'true',
        },
        top_level_method_header='create_user_bonus',
        low_level_method_header='create_user_bonus',
    )


def test_create_user_bonus_sync_via_async_retry(
    respx_mock, toloka_client, toloka_url, user_bonus_map, user_bonus_map_with_readonly,
    create_user_bonus_operation_success, create_user_bonus_log,
):
    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonus,
        create_method_kwargs={'user_bonus': UserBonus.structure(user_bonus_map)},
        returned_object=simplejson.dumps(user_bonus_map_with_readonly),
        expected_response_object=UserBonus.structure(user_bonus_map_with_readonly),
        success_operation_map=create_user_bonus_operation_success,
        operation_log=create_user_bonus_log,
        create_object_path='user-bonuses',
        get_object_path=f'user-bonuses/{user_bonus_map_with_readonly["id"]}',
    )


def test_create_user_bonus_sync_via_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url,
    user_bonus_map, create_user_bonus_operation_fail,
    operation_id
):
    user_bonus = client.structure(user_bonus_map, client.user_bonus.UserBonus)
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonus,
        create_method_kwargs={
            'user_bonus': user_bonus,
            'operation_id': operation_id,
        },
        failed_operation_map=create_user_bonus_operation_fail,
        create_object_path='user-bonuses',
    )


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
        {'user_id': 'user-1', 'amount': 1.50},
        {'user_id': 'user-2', 'amount': 2.00},
    ]


@pytest.fixture
def user_bonus_map_async_with_read_only(user_bonus_map_async):
    return [{**user_bonus_map, 'id': f'user-bonus-{i + 1}'} for i, user_bonus_map in enumerate(user_bonus_map_async)]


@pytest.fixture
def create_user_bonuses_operation_id() -> UUID:
    return UUID('09ee3f76-5cdc-4388-adcc-c580a3ab4c53')


@pytest.fixture
def create_user_bonuses_operation_running(create_user_bonuses_operation_id):
    return {
        'id': str(create_user_bonuses_operation_id),
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
def create_user_bonuses_operation_fail(create_user_bonuses_operation_running):
    return {**create_user_bonuses_operation_running, 'status': 'FAIL'}


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
    create_user_bonuses_operation_running, create_user_bonuses_operation_success, create_user_bonuses_log,
    user_bonuses_result_map
):
    assert_sync_via_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses,
        create_method_kwargs={
            'user_bonuses': client.structure(user_bonus_map_async, List[UserBonus]),
            'operation_id': create_user_bonuses_operation_id
        },
        returned_object=simplejson.dumps({'items': user_bonus_map_async_with_read_only, 'has_more': False}),
        expected_response_object=UserBonusBatchCreateResult.structure(user_bonuses_result_map),
        operation_log=simplejson.dumps(create_user_bonuses_log),
        create_object_path='user-bonuses',
        get_object_path='user-bonuses',
        operation_running=Operation.structure(create_user_bonuses_operation_running),
        success_operation=Operation.structure(create_user_bonuses_operation_success),
        expected_query_params={
            'async_mode': 'true',
            'operation_id': str(create_user_bonuses_operation_id),
        },
        top_level_method_header='create_user_bonuses',
        low_level_method_header='create_user_bonuses',
    )


def test_create_user_bonuses_sync_via_async_retry(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    user_bonus_map_async, create_user_bonuses_operation_id, user_bonus_map_async_with_read_only,
    create_user_bonuses_operation_success, create_user_bonuses_log,
    user_bonuses_result_map
):
    user_bonuses = [
        client.structure(user_bonus_map, client.user_bonus.UserBonus)
        for user_bonus_map in user_bonus_map_async
    ]

    assert_retried_sync_via_async_object_creation_returns_already_existing_object(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses,
        create_method_kwargs={'user_bonuses': user_bonuses},
        returned_object=simplejson.dumps({'items': user_bonus_map_async_with_read_only, 'has_more': False}),
        expected_response_object=UserBonusBatchCreateResult.structure(user_bonuses_result_map),
        success_operation_map=create_user_bonuses_operation_success,
        operation_log=create_user_bonuses_log,
        create_object_path='user-bonuses',
        get_object_path='user-bonuses',
    )


def test_create_user_bonuses_sync_via_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, no_uuid_random,
    user_bonus_map_async, create_user_bonuses_operation_id, user_bonus_map_async_with_read_only,
    create_user_bonuses_operation_fail, create_user_bonuses_log,
    user_bonuses_result_map
):
    user_bonuses = [
        client.structure(user_bonus_map, client.user_bonus.UserBonus)
        for user_bonus_map in user_bonus_map_async
    ]

    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses,
        create_method_kwargs={'user_bonuses': user_bonuses},
        failed_operation_map=create_user_bonuses_operation_fail,
        create_object_path='user-bonuses',
    )


def test_create_user_bonuses_async(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonuses_operation_id,
    create_user_bonus_operation_running
):
    assert_async_object_creation_is_successful(
        respx_mock=respx_mock,
        toloka_client=toloka_client,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses_async,
        create_method_kwargs={
            'user_bonuses': client.structure(user_bonus_map_async, List[client.UserBonus]),
            'operation_id': create_user_bonuses_operation_id,
        },
        create_object_path='user-bonuses',
        success_operation_map=create_user_bonus_operation_running,
        expected_query_params={
            'async_mode': 'true',
            'operation_id': str(create_user_bonuses_operation_id),
        },
        top_level_method_header='create_user_bonuses_async',
        low_level_method_header='create_user_bonuses_async',
    )


def test_create_user_bonuses_async_retry(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonus_operation_running
):
    assert_retried_async_object_creation_returns_existing_operation(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses_async,
        create_method_kwargs={
            'user_bonuses': client.structure(user_bonus_map_async, List[client.UserBonus]),
        },
        create_object_path='user-bonuses',
        success_operation_map=create_user_bonus_operation_running,
    )


def test_create_user_bonuses_async_retry_failed_operation(
    respx_mock, toloka_client, toloka_url, user_bonus_map_async, create_user_bonus_operation_fail
):
    assert_retried_failed_operation_fails_with_failed_operation_exception(
        respx_mock=respx_mock,
        toloka_url=toloka_url,
        create_method=toloka_client.create_user_bonuses_async,
        create_method_kwargs={
            'user_bonuses': client.structure(user_bonus_map_async, List[client.UserBonus]),
        },
        failed_operation_map=create_user_bonus_operation_fail,
        create_object_path='user-bonuses',
    )
