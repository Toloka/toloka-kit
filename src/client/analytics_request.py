from enum import Enum, unique

from .primitives.base import attribute, BaseTolokaObject


class AnalyticsRequest(BaseTolokaObject, spec_field='subject', spec_enum='Subject'):

    @unique
    class Subject(Enum):
        POOL = 'POOL'

    subject_id: str = attribute(required=True)


class PoolAnalyticsRequest(
    AnalyticsRequest,
    spec_value=AnalyticsRequest.Subject.POOL,
    spec_field='name',
    spec_enum='Subject'
):

    @unique
    class Subject(Enum):
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


class RealTasksCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.REAL_TASKS_COUNT):
    pass


class SubmitedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SUBMITTED_ASSIGNMENTS_COUNT):
    pass


class SkippedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SKIPPED_ASSIGNMENTS_COUNT):
    pass


class RejectedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.REJECTED_ASSIGNMENTS_COUNT):
    pass


class ApprovedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.APPROVED_ASSIGNMENTS_COUNT):
    pass


class CompletionPercentagePoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.COMPLETION_PERCENTAGE):
    pass


class AvgSubmitAssignmentMillisPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.AVG_SUBMIT_ASSIGNMENT_MILLIS):
    pass


class SpentBudgetPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.SPENT_BUDGET):
    pass


class UniqueWorkersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_WORKERS_COUNT):
    pass


class UniqueSubmittersCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.UNIQUE_SUBMITTERS_COUNT):
    pass


class ActiveWorkersByFilterCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ACTIVE_WORKERS_BY_FILTER_COUNT):
    interval_hours: int = attribute(required=True)


class EstimatedAssignmentsCountPoolAnalytics(PoolAnalyticsRequest, spec_value=PoolAnalyticsRequest.Subject.ESTIMATED_ASSIGNMENTS_COUNT):
    pass
