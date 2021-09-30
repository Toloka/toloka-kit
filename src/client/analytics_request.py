__all__ = [
    'AnalyticsRequest',
    'PoolAnalyticsRequest',
    'RealTasksCountPoolAnalytics',
    'SubmitedAssignmentsCountPoolAnalytics',
    'SkippedAssignmentsCountPoolAnalytics',
    'RejectedAssignmentsCountPoolAnalytics',
    'ApprovedAssignmentsCountPoolAnalytics',
    'CompletionPercentagePoolAnalytics',
    'AvgSubmitAssignmentMillisPoolAnalytics',
    'SpentBudgetPoolAnalytics',
    'UniqueWorkersCountPoolAnalytics',
    'UniqueSubmittersCountPoolAnalytics',
    'ActiveWorkersByFilterCountPoolAnalytics',
    'EstimatedAssignmentsCountPoolAnalytics'
]
from enum import unique

from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._docstrings import inherit_docstrings
from ..util._extendable_enum import ExtendableStrEnum


class AnalyticsRequest(BaseTolokaObject, spec_field='subject', spec_enum='Subject'):
    """Base class for all analytics requests in Toloka

    How to use this requests and get some useful information see in example in "TolokaClient.get_analytics".

    Attributes:
        subject_id: ID of the object you want to get analytics about.
    """
    @unique
    class Subject(ExtendableStrEnum):
        POOL = 'POOL'

    subject_id: str = attribute(required=True)


@inherit_docstrings
class PoolAnalyticsRequest(
    AnalyticsRequest,
    spec_value=AnalyticsRequest.Subject.POOL,
    spec_field='name',
    spec_enum='Subject'
):
    """Base class for all analytics requests about pools

    Right now you can get analytics only about pool.
    """

    @unique
    class Subject(ExtendableStrEnum):
        REAL_TASKS_COUNT = 'real_tasks_count'
        SUBMITTED_ASSIGNMENTS_COUNT = 'submitted_assignments_count'
        SKIPPED_ASSIGNMENTS_COUNT = 'skipped_assignments_count'
        REJECTED_ASSIGNMENTS_COUNT = 'rejected_assignments_count'
        APPROVED_ASSIGNMENTS_COUNT = 'approved_assignments_count'
        COMPLETION_PERCENTAGE = 'completion_percentage'
        AVG_SUBMIT_ASSIGNMENT_MILLIS = 'avg_submit_assignment_millis'
        SPENT_BUDGET = 'spent_budget'
        UNIQUE_WORKERS_COUNT = 'unique_workers_count'
        UNIQUE_SUBMITTERS_COUNT = 'unique_submitters_count'
        ACTIVE_WORKERS_BY_FILTER_COUNT = 'active_workers_by_filter_count'
        ESTIMATED_ASSIGNMENTS_COUNT = 'estimated_assignments_count'


@inherit_docstrings
class RealTasksCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.REAL_TASKS_COUNT):
    """The number of tasks in the pool

    It does not take into account the overlap, how many tasks will be on one page, or the presence of golden tasks.
    """
    pass


@inherit_docstrings
class SubmitedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SUBMITTED_ASSIGNMENTS_COUNT):
    """Number of assignments in the "submited" status in the pool

    Do not confuse it with the approved status.
    "Submited" status means that the task was completed by the performer and send for review.
    "Approved" status means that the task has passed review and money has been paid for it.
    """
    pass


@inherit_docstrings
class SkippedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SKIPPED_ASSIGNMENTS_COUNT):
    """Number of assignments in the "skipped" status in the pool
    """
    pass


@inherit_docstrings
class RejectedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.REJECTED_ASSIGNMENTS_COUNT):
    """Number of assignments in the "rejected" status in the pool
    """
    pass


@inherit_docstrings
class ApprovedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.APPROVED_ASSIGNMENTS_COUNT):
    """Number of assignments in the "approved" status in the pool

    Do not confuse it with the submited status.
    "Submited" status means that the task was completed by the performer and send for review.
    "Approved" status means that the task has passed review and money has been paid for it.
    """
    pass


@inherit_docstrings
class CompletionPercentagePoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.COMPLETION_PERCENTAGE):
    """Approximate percentage of completed tasks in the pool
    """
    pass


@inherit_docstrings
class AvgSubmitAssignmentMillisPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.AVG_SUBMIT_ASSIGNMENT_MILLIS):
    """Average time to complete one task page in milliseconds
    """
    pass


@inherit_docstrings
class SpentBudgetPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SPENT_BUDGET):
    """How much money has already been spent on this pool, excluding fee
    """
    pass


@inherit_docstrings
class UniqueWorkersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_WORKERS_COUNT):
    """The number of unique performers who took tasks from the pool
    """
    pass


@inherit_docstrings
class UniqueSubmittersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_SUBMITTERS_COUNT):
    """The number of unique performers who have submitted to the pool
    """
    pass


@inherit_docstrings
class ActiveWorkersByFilterCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ACTIVE_WORKERS_BY_FILTER_COUNT):
    """The number of active performers matching the pool filters for the last hours

    Attributes:
        interval_hours: The number of hours to take into account when collecting statistics.
    """
    interval_hours: int = attribute(required=True)


@inherit_docstrings
class EstimatedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ESTIMATED_ASSIGNMENTS_COUNT):
    """The approximate number of responses to task pages.
    """
    pass
