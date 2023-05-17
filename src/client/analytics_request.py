__all__ = [
    'AnalyticsRequest',
    'PoolAnalyticsRequest',
    'RealTasksCountPoolAnalytics',
    'SubmittedAssignmentsCountPoolAnalytics',
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
    """A base class for analytics requests.

    Make analytics requests to Toloka with the [get_analytics](toloka.client.TolokaClient.get_analytics.md) method.

    Attributes:
        subject_id: The ID of an object to get analytics about.
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
    """A base class for analytics requests about pools.

    Attributes:
        subject_id: The ID of a pool to get analytics about.
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
    """Counts the number of general tasks in a pool.

    Note, that `RealTasksCountPoolAnalytics` doesn't take into account control and training tasks, and task overlap.
    """
    pass


@inherit_docstrings
class SubmittedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SUBMITTED_ASSIGNMENTS_COUNT):
    """Counts the total number of completed assignments in a pool.

    It counts assignments with the `SUBMITTED`, `ACCEPTED`, or `REJECTED` status.
    """
    pass


@inherit_docstrings
class SkippedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SKIPPED_ASSIGNMENTS_COUNT):
    """Counts the number of assignments with the `SKIPPED` status in a pool.
    """
    pass


@inherit_docstrings
class RejectedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.REJECTED_ASSIGNMENTS_COUNT):
    """Counts the number of assignments with the `REJECTED` status in a pool.
    """
    pass


@inherit_docstrings
class ApprovedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.APPROVED_ASSIGNMENTS_COUNT):
    """Counts the number of assignments with the `ACCEPTED` status in a pool.

    Do not confuse these task statuses:
        * `SUBMITTED` tasks are completed by Tolokers and sent for a review.
        * `ACCEPTED` tasks have passed the review and have been paid for.
    """
    pass


@inherit_docstrings
class CompletionPercentagePoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.COMPLETION_PERCENTAGE):
    """Calculates the percentage of completed tasks in a pool.
    """
    pass


@inherit_docstrings
class AvgSubmitAssignmentMillisPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.AVG_SUBMIT_ASSIGNMENT_MILLIS):
    """Calculates the average time in milliseconds for completing one task suite.
    """
    pass


@inherit_docstrings
class SpentBudgetPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SPENT_BUDGET):
    """Shows money spent on a pool, excluding fees.
    """
    pass


@inherit_docstrings
class UniqueWorkersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_WORKERS_COUNT):
    """Counts the number of Tolokers who took tasks from a pool.
    """
    pass


@inherit_docstrings
class UniqueSubmittersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_SUBMITTERS_COUNT):
    """Counts the number of Tolokers who completed at least one task suite in a pool.
    """
    pass


@inherit_docstrings
class ActiveWorkersByFilterCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ACTIVE_WORKERS_BY_FILTER_COUNT):
    """Counts the number of active Tolokers that match pool filters.

    Active Tolokers are Tolokers who viewed and completed tasks recently.

    Attributes:
        interval_hours: The interval in hours to take into account.
    """
    interval_hours: int = attribute(required=True)


@inherit_docstrings
class EstimatedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ESTIMATED_ASSIGNMENTS_COUNT):
    """The approximate number of responses to task pages.
    """
    pass
