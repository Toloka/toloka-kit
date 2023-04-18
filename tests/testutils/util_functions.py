import re
from typing import Callable, Optional

import httpx
from toloka import client as client
from toloka.client.exceptions import IncorrectActionsApiError
from toloka.client.primitives.base import BaseTolokaObject


def check_headers(request, expected_headers):
    if isinstance(request, httpx.Request):
        assert set((key.lower(), value.lower()) for key, value in expected_headers.items()) <= request.headers.items()
    else:
        assert expected_headers.items() <= request._request.headers.items()


def assert_retried_object_creation_returns_already_existing_object(
    respx_mock,
    toloka_url: str,
    create_method: Callable,
    create_method_kwargs: dict,
    get_object_side_effect: Optional[Callable],
    expected_response_object: BaseTolokaObject,
    success_operation_map: dict,
    operation_log: Optional[list],
    create_object_path: str,
    get_object_path: str,
) -> None:
    requests_count = 0
    first_request_op_id = None

    def create_object(request):
        nonlocal requests_count
        nonlocal first_request_op_id

        requests_count += 1
        if requests_count == 1:
            first_request_op_id = request.url.params['operation_id']
            expected_operation_id = create_method_kwargs.get('operation_id')
            if expected_operation_id:
                assert first_request_op_id == expected_operation_id
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
    ).mock(httpx.Response(json=success_operation_map, status_code=201))

    if operation_log is not None:
        respx_mock.get(re.compile(rf'{toloka_url}/operations/.*/log')).mock(
            httpx.Response(json=operation_log, status_code=201)
        )

    if get_object_side_effect is not None:
        respx_mock.get(f'{toloka_url}/{get_object_path}').mock(side_effect=get_object_side_effect)

    result = create_method(**create_method_kwargs)

    assert expected_response_object == result
    assert requests_count == 2
