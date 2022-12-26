from decimal import Decimal

import httpx
import simplejson

import pytest
import toloka.client as client

from .testutils.util_functions import check_headers


@pytest.fixture
def task_operation_log_list():
    return [
        {
            "input": {
                "input_values": {
                    "imagis": "https://image/3.jpg",
                },
                "pool_id": "20646589",
            },
            "output": {
                "input_values.image": {
                    "code": "VALUE_REQUIRED",
                    "message": "Value must be present and not equal to null",
                },
                "input_values.imagis": {
                    "code": "VALUE_NOT_ALLOWED",
                    "message": "Unknown field name",
                }
            },
            "success": False,
            "type": "TASK_VALIDATE",
        },
        {
            "input": {
                "infinite_overlap": False,
                "input_values": {
                    "image": "https://image/1.jpg",
                },
                "overlap": 1,
                "pool_id": "20646589",
            },
            "output": {
                "task_id": "00013b0abd--6008446fe335ad39b8920ee4",
            },
            "success": True,
            "type": "TASK_CREATE",
        },
        {
            "input": {
                "infinite_overlap": False,
                "input_values": {
                    "image": "https://image/2.jpg",
                },
                "overlap": 1,
                "pool_id": "20646589",
            },
            "output": {
                "task_id": "00013b0abd--6008446fe335ad39b8920ee6",
            },
            "success": True,
            "type": "TASK_CREATE",
        },
    ]


@pytest.fixture
def bonus_operation_log_list():
    return [
        {
            "input": {
                "amount": Decimal('0.01'),
                "public_title": {
                    "RU": "Молодец!",
                },
                "user_id": "66630d1001d3745aee7de3f3060666649",
            },
            "output": {
                "user_bonus_id": "1300060",
            },
            "success": True,
            "type": "USER_BONUS_PERSIST",
        },
        {
            "input": {
                "amount": Decimal('0.01'),
                "public_title": {
                    "RU": "Молодец!",
                },
                "user_id": "user-1",
            },
            "output": {
                "user_id": {
                    "code": "ENTITY_DOES_NOT_EXIST",
                    "message": "Entity does not exist",
                }
            },
            "success": False,
            "type": "USER_BONUS_VALIDATE",
        },
    ]


@pytest.fixture
def tasks_suite_operation_log_list():
    return [
        {
            "input": {
                "infinite_overlap": False,
                "overlap": 1,
                "pool_id": "20646589",
                "tasks": [
                    {
                        "input_values": {
                            "imagis": "http://images.com/3.png",
                        }
                    }
                ]
            },
            "output": {
                "tasks.0.input_values.image": {
                    "code": "VALUE_REQUIRED",
                    "message": "Value must be present and not equal to null",
                },
                "tasks.0.input_values.imagis": {
                    "code": "VALUE_NOT_ALLOWED",
                    "message": "Unknown field name",
                }
            },
            "success": False,
            "type": "TASK_SUITE_VALIDATE",
        },
        {
            "input": {
                "infinite_overlap": False,
                "overlap": 1,
                "pool_id": "20646589",
                "tasks": [
                    {
                        "input_values": {
                            "image": "http://images.com/1.png",
                        }
                    }
                ]
            },
            "output": {
                "task_suite_id": "00013b0abd--60094b06c680984b001e5040",
            },
            "success": True,
            "type": "TASK_SUITE_CREATE",
        },
        {
            "input": {
                "infinite_overlap": False,
                "overlap": 1,
                "pool_id": "20646589",
                "tasks": [
                    {
                        "input_values": {
                            "image": "http://images.com/2.png",
                        }
                    }
                ]
            },
            "output": {
                "task_suite_id": "00013b0abd--60094b06c680984b001e5047",
            },
            "success": True,
            "type": "TASK_SUITE_CREATE",
        }
    ]


@pytest.mark.parametrize(
    'object',
    [
        'task',
        'bonus',
        'tasks_suite',
    ],
)
def test_get_operagiton_log(request, respx_mock, toloka_client, toloka_url, object):
    log_list = request.getfixturevalue(f'{object}_operation_log_list')
    operation_id = 'ee60ef13-37a3-666a-9220-266daa4b71a7'

    def get_operation_log(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_operation_log',
            'X-Low-Level-Method': 'get_operation_log',
        }
        check_headers(request, expected_headers)

        return httpx.Response(text=simplejson.dumps(log_list), status_code=201)

    respx_mock.get(f'{toloka_url}/operations/{operation_id}/log').mock(side_effect=get_operation_log)
    result = toloka_client.get_operation_log(operation_id)
    assert log_list == client.unstructure(result)
