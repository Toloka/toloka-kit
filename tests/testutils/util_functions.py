import re
from typing import Callable, Optional, Union

import httpx
import pytest
from httpx import QueryParams
from toloka import client as client
from toloka.client.exceptions import FailedOperation, IncorrectActionsApiError
from toloka.client.operations import Operation
from toloka.client.primitives.base import BaseTolokaObject


def check_headers(request, expected_headers):
    if isinstance(request, httpx.Request):
        assert set((key.lower(), value.lower()) for key, value in expected_headers.items()) <= request.headers.items()
    else:
        assert expected_headers.items() <= request._request.headers.items()


def assert_sync_via_async_object_creation_is_successful(
    respx_mock,
    toloka_client,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    returned_object: Union[str, dict, Callable],
    expected_response_object: BaseTolokaObject,
    operation_log: Union[list, str],
    create_object_path: str,
    get_object_path: str,
    operation_running: Operation,
    success_operation: Operation,
    expected_query_params: dict,
    top_level_method_header: str,
    low_level_method_header: str,
):
    def create_object(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': top_level_method_header,
            'X-Low-Level-Method': low_level_method_header,
        }
        check_headers(request, expected_headers)
        assert QueryParams(**expected_query_params) == request.url.params
        return httpx.Response(json=operation_running.unstructure(), status_code=201)

    respx_mock.post(f'{toloka_url}/{create_object_path}').mock(side_effect=create_object)
    respx_mock.get(url__regex=rf'{toloka_url}/operations/.*(?<!log)$').mock(
        httpx.Response(json=success_operation.unstructure(), status_code=201)
    )

    if isinstance(operation_log, list):
        log_response = httpx.Response(json=operation_log, status_code=201)
    else:
        log_response = httpx.Response(text=operation_log, status_code=201)
    respx_mock.get(re.compile(rf'{toloka_url}/operations/.*/log')).mock(log_response)

    if isinstance(returned_object, dict):
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(httpx.Response(json=returned_object, status_code=200))
    elif isinstance(returned_object, str):
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(httpx.Response(text=returned_object, status_code=200))
    else:
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(side_effect=returned_object)

    result = create_method(**create_method_kwargs)
    assert result == expected_response_object


def assert_async_object_creation_is_successful(
    respx_mock,
    toloka_client,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    create_object_path: str,
    success_operation_map: dict,
    expected_query_params: dict,
    top_level_method_header: str,
    low_level_method_header: str,
):
    def create_object(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': top_level_method_header,
            'X-Low-Level-Method': low_level_method_header,
        }
        check_headers(request, expected_headers)
        assert QueryParams(**{**expected_query_params, 'operation_id': request.url.params['operation_id']}) \
               == request.url.params
        return httpx.Response(json=success_operation_map, status_code=200)

    respx_mock.post(f'{toloka_url}/{create_object_path}').mock(side_effect=create_object)
    respx_mock.get(url__regex=rf'{toloka_url}/operations/.*(?<!log)$').mock(
        httpx.Response(json=success_operation_map, status_code=201)
    )

    result = create_method(**create_method_kwargs)
    assert result.unstructure() == success_operation_map


def assert_retried_async_object_creation_returns_existing_operation(
    respx_mock,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    create_object_path: str,
    success_operation_map: dict,
):
    requests_count = 0
    first_request_op_id = None

    def create_object(request):
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
    ).mock(httpx.Response(json=success_operation_map, status_code=200))
    respx_mock.post(f'{toloka_url}/{create_object_path}').mock(side_effect=create_object)

    result = create_method(**create_method_kwargs)
    assert requests_count == 2
    assert result == Operation.structure(success_operation_map)


def assert_retried_sync_via_async_object_creation_returns_already_existing_object(
    respx_mock,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    returned_object: Union[str, dict, Callable],
    expected_response_object: BaseTolokaObject,
    success_operation_map: dict,
    operation_log: Optional[list],
    create_object_path: str,
    get_object_path: str,
) -> None:
    requests_counter = _mock_faulty_object_creation_environment(
        create_object_path=create_object_path,
        get_object_path=get_object_path,
        returned_object=returned_object,
        operation_log=operation_log,
        respx_mock=respx_mock,
        operation_map=success_operation_map,
        toloka_url=toloka_url,
        create_method_kwargs=create_method_kwargs,
    )

    result = create_method(**create_method_kwargs)

    assert result == expected_response_object
    assert requests_counter.value == 2


def assert_retried_failed_operation_fails_with_failed_operation_exception(
    respx_mock,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    failed_operation_map: dict,
    create_object_path: str,
):
    requests_counter = _mock_faulty_object_creation_environment(
        create_object_path=create_object_path,
        respx_mock=respx_mock,
        operation_map=failed_operation_map,
        toloka_url=toloka_url,
        get_object_path='',
        create_method_kwargs=create_method_kwargs,
        operation_log=None,
        returned_object=lambda: ...,
    )

    with pytest.raises(FailedOperation):
        create_method(**create_method_kwargs)

    assert requests_counter.value == 2


class Counter:
    def __init__(self):
        self.value = 0


def _mock_faulty_object_creation_environment(
    create_object_path,
    get_object_path,
    returned_object: Union[str, Callable, dict],
    operation_log,
    respx_mock,
    operation_map,
    toloka_url,
    create_method_kwargs,
):
    requests_count = Counter()
    first_request_op_id = None

    def create_object(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count.value += 1
        if requests_count.value == 1:
            first_request_op_id = request.url.params['operation_id']
            expected_operation_id = create_method_kwargs.get('operation_id')
            if expected_operation_id:
                assert first_request_op_id == str(expected_operation_id)
            return httpx.Response(status_code=500)

        assert request.url.params['operation_id'] == str(first_request_op_id)

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

    respx_mock.post(f'{toloka_url}/{create_object_path}').mock(side_effect=create_object)
    respx_mock.get(
        url__regex=rf'{toloka_url}/operations/.*(?<!log)$'
    ).mock(httpx.Response(json=operation_map, status_code=201))
    if operation_log is not None:
        respx_mock.get(re.compile(rf'{toloka_url}/operations/.*/log')).mock(
            httpx.Response(json=operation_log, status_code=201)
        )
    if isinstance(returned_object, dict):
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(
            httpx.Response(json=returned_object, status_code=201)
        )
    elif isinstance(returned_object, str):
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(
            httpx.Response(text=returned_object, status_code=201)
        )
    else:
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(side_effect=returned_object)
    return requests_count
