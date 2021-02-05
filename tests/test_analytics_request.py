import pytest
import toloka.client as client
from toloka.client.analytics_request import (
    RealTasksCountPoolAnalytics,
    SubmitedAssignmentsCountPoolAnalytics,
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


def test_send_analytics_request(requests_mock, toloka_client, toloka_api_url, full_tasks_request_map, simple_answer_map):

    def task_suites(request, context):
        assert full_tasks_request_map == request.json()
        return simple_answer_map
    requests_mock.post(f'{toloka_api_url}/staging/analytics-2', json=task_suites)

    stat_requests = [
        RealTasksCountPoolAnalytics(subject_id='123'),
        SubmitedAssignmentsCountPoolAnalytics(subject_id='123'),
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
