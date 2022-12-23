import json

import httpx
import pytest
import toloka.client as client
from toloka.client.analytics_request import (
    RealTasksCountPoolAnalytics,
    SubmittedAssignmentsCountPoolAnalytics,
    SkippedAssignmentsCountPoolAnalytics,
    RejectedAssignmentsCountPoolAnalytics,
    ApprovedAssignmentsCountPoolAnalytics,
    CompletionPercentagePoolAnalytics,
    AvgSubmitAssignmentMillisPoolAnalytics,
    SpentBudgetPoolAnalytics,
    UniqueWorkersCountPoolAnalytics,
    UniqueSubmittersCountPoolAnalytics,
    ActiveWorkersByFilterCountPoolAnalytics,
    EstimatedAssignmentsCountPoolAnalytics,
)

from .testutils.util_functions import check_headers


@pytest.fixture
def full_tasks_request_map():
    return [
        {
            "name": "real_tasks_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "submitted_assignments_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "skipped_assignments_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "rejected_assignments_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "approved_assignments_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "completion_percentage",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "avg_submit_assignment_millis",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "spent_budget",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "unique_workers_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "unique_submitters_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "name": "estimated_assignments_count",
            "subject": "POOL",
            "subject_id": "123"
        },
        {
            "interval_hours": 10,
            "name": "active_workers_by_filter_count",
            "subject": "POOL",
            "subject_id": "123"
        }
    ]


@pytest.fixture
def simple_answer_map():
    return {
        "id": "6f38905cc-4e04-666d-8264-123552147ba0",
        "parameters": {
            "value": [
                {
                    "name": "real_tasks_count",
                    "subject": "POOL",
                    "subject_id": "123"
                },
            ]
        },
        "progress": 0,
        "status": "PENDING",
        "submitted": "2020-02-01T13:14:15",
        "type": "ANALYTICS"
    }


@pytest.fixture
def success_answer_map():
    return {
        'id': '8ee7e276-53bb-4220-823e-05f578392915',
        'type': 'ANALYTICS',
        'status': 'SUCCESS',
        'submitted': '2021-08-24T06:30:08.394',
        'started': '2021-08-24T06:30:08.51',  # 2 ms digits
        'finished': '2021-08-24T06:30:11.99999',  # 5 ms digits
        'progress': 100, 'parameters':
        {
            'value':
            [
                {'name': 'submitted_assignments_count', 'subject': 'POOL', 'subject_id': '26807107'},
            ]
        },
        'details':
        {
            'value':
            [
                {
                    'result': 75,
                    'request':
                    {
                        'name': 'submitted_assignments_count',
                        'subject': 'POOL',
                        'subject_id': '26807107'
                    },
                    'finished': '2021-08-24T06:30:08.923461'
                },
            ]
        }
    }


def test_send_analytics_request(respx_mock, toloka_client, toloka_api_url,
                                      full_tasks_request_map, simple_answer_map):

    def task_suites(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_analytics',
            'X-Low-Level-Method': 'get_analytics',
        }
        check_headers(request, expected_headers)

        assert full_tasks_request_map == json.loads(request.content)
        return httpx.Response(status_code=200, json=simple_answer_map)

    respx_mock.post(f'{toloka_api_url}/staging/analytics-2').mock(side_effect=task_suites)

    stat_requests = [
        RealTasksCountPoolAnalytics(subject_id='123'),
        SubmittedAssignmentsCountPoolAnalytics(subject_id='123'),
        SkippedAssignmentsCountPoolAnalytics(subject_id='123'),
        RejectedAssignmentsCountPoolAnalytics(subject_id='123'),
        ApprovedAssignmentsCountPoolAnalytics(subject_id='123'),
        CompletionPercentagePoolAnalytics(subject_id='123'),
        AvgSubmitAssignmentMillisPoolAnalytics(subject_id='123'),
        SpentBudgetPoolAnalytics(subject_id='123'),
        UniqueWorkersCountPoolAnalytics(subject_id='123'),
        UniqueSubmittersCountPoolAnalytics(subject_id='123'),
        EstimatedAssignmentsCountPoolAnalytics(subject_id='123'),
        ActiveWorkersByFilterCountPoolAnalytics(subject_id='123', interval_hours=10),
    ]

    operation = toloka_client.get_analytics(stat_requests)
    assert simple_answer_map == client.unstructure(operation)


def test_less_ms_digits(respx_mock, toloka_client, toloka_api_url, success_answer_map):
    real_result = {
        **success_answer_map,
        'submitted': '2021-08-24T06:30:08.394000',  # 6 ms digits
        'started': '2021-08-24T06:30:08.510000',    # 6 ms digits
        'finished': '2021-08-24T06:30:11.999990',   # 6 ms digits
    }

    def task_map(request):
        expected_headers = {
            'X-Caller-Context': 'client' if isinstance(toloka_client, client.TolokaClient) else 'async_client',
            'X-Top-Level-Method': 'get_analytics',
            'X-Low-Level-Method': 'get_analytics',
        }
        check_headers(request, expected_headers)

        return httpx.Response(status_code=200, json=success_answer_map)

    respx_mock.post(f'{toloka_api_url}/staging/analytics-2').mock(side_effect=task_map)
    operation = toloka_client.get_analytics([SubmittedAssignmentsCountPoolAnalytics(subject_id='123')])
    assert real_result == client.unstructure(operation)
