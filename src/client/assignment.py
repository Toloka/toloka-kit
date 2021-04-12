__all__ = [
    'Assignment',
    'AssignmentPatch',
    'GetAssignmentsTsvParameters'
]
from attr.validators import optional, instance_of
import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import List, Optional

from .primitives.base import attribute, BaseTolokaObject
from .primitives.parameter import Parameters
from .solution import Solution
from .task import Task


class Assignment(BaseTolokaObject):
    """Contains information about an assigned task suite and the results

    Attributes:
        id: ID of the task suite assignment to a performer.
        task_suite_id: ID of a task suite.
        pool_id: ID of the pool that the task suite belongs to.
        user_id: ID of the performer who was assigned the task suite.
        status: Status of an assigned task suite.
            * ACTIVE - In the process of execution by the performer.
            * SUBMITTED - Completed but not checked.
            * ACCEPTED - Accepted by the requester.
            * REJECTED - Rejected by the requester.
            * SKIPPED - Skipped by the performer.
            * EXPIRED - The time for completing the tasks expired.
        reward: Payment received by the performer.
        tasks: Data for the tasks.
        automerged: Flag of the response received as a result of merging identical tasks. Value:
            * True - The response was recorded when identical tasks were merged.
            * False - Normal performer response.
        created: The date and time when the task suite was assigned to a performer.
        submitted: The date and time when the task suite was completed by a performer.
        accepted: The date and time when the responses for the task suite were accepted by the requester.
        rejected: The date and time when the responses for the task suite were rejected by the requester.
        skipped: The date and time when the task suite was skipped by the performer.
        expired: The date and time when the time for completing the task suite expired.
        first_declined_solution_attempt: For training tasks. The performer's first responses in the training task
            (only if these were the wrong answers). If the performer answered correctly on the first try, the
            first_declined_solution_attempt array is omitted.
            Arrays with the responses (output_values) are arranged in the same order as the task data in the tasks array.
        solutions: performer responses. Arranged in the same order as the data for tasks in the tasks array.
        mixed: Type of operation for creating a task suite:
            * True - Automatic ("smart mixing").
            * False - Manually.
        public_comment: Public comment about an assignment. Why it was accepted or rejected.
    """

    @unique
    class Status(Enum):
        ACTIVE = 'ACTIVE'
        SUBMITTED = 'SUBMITTED'
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'
        SKIPPED = 'SKIPPED'
        EXPIRED = 'EXPIRED'

    ACTIVE = Status.ACTIVE
    SUBMITTED = Status.SUBMITTED
    ACCEPTED = Status.ACCEPTED
    REJECTED = Status.REJECTED
    SKIPPED = Status.SKIPPED
    EXPIRED = Status.EXPIRED

    id: str
    task_suite_id: str
    pool_id: str
    user_id: str
    status: Status
    reward: Decimal = attribute(validator=optional(instance_of(Decimal)))
    tasks: List[Task]
    automerged: bool

    created: datetime.datetime
    submitted: datetime.datetime
    accepted: datetime.datetime
    rejected: datetime.datetime
    skipped: datetime.datetime
    expired: datetime.datetime

    first_declined_solution_attempt: List[Solution]
    solutions: List[Solution]
    mixed: bool

    public_comment: str


class AssignmentPatch(BaseTolokaObject):
    """Allows you to accept or reject tasks, and leave a comment

    Used in "TolokaClient.patch_assignment" method.

    Attributes:
        public_comment: Public comment about an assignment. Why it was accepted or rejected.
        status: Status of an assigned task suite.
            * ACCEPTED - Accepted by the requester.
            * REJECTED - Rejected by the requester.
    """
    public_comment: str
    status: Assignment.Status


class GetAssignmentsTsvParameters(Parameters):
    """Allows you to downloads assignments as pandas.DataFrame

    Used in "TolokaClient.get_assignments_df" method.
    Implements the same behavior as if you download results in web-interface and then read it by pandas.

    Attributes:
        status: Assignments in which statuses will be downloaded.
        start_time_from: Upload assignments submitted after the specified date and time.
        start_time_to: Upload assignments submitted before the specified date and time.
        exclude_banned: Exclude answers from banned performers, even if assignments in suitable status "ACCEPTED".
        field: The names of the fields to be unloaded. Only the field names from the Assignment class, all other fields
            are added by default.
    """

    @unique
    class Status(Enum):
        ACTIVE = 'ACTIVE'
        SUBMITTED = 'SUBMITTED'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'
        SKIPPED = 'SKIPPED'
        EXPIRED = 'EXPIRED'

    @unique
    class Field(Enum):
        LINK = 'ASSIGNMENT:link'
        ASSIGNMENT_ID = 'ASSIGNMENT:assignment_id'
        TASK_SUITE_ID = 'ASSIGNMENT:task_suite_id'
        WORKER_ID = 'ASSIGNMENT:worker_id'
        STATUS = 'ASSIGNMENT:status'
        STARTED = 'ASSIGNMENT:started'
        SUBMITTED = 'ASSIGNMENT:submitted'
        ACCEPTED = 'ASSIGNMENT:accepted'
        REJECTED = 'ASSIGNMENT:rejected'
        SKIPPED = 'ASSIGNMENT:skipped'
        EXPIRED = 'ASSIGNMENT:expired'
        REWARD = 'ASSIGNMENT:reward'

    _default_status = [Status.APPROVED]
    _default_fields = [Field.LINK, Field.ASSIGNMENT_ID, Field.WORKER_ID, Field.STATUS, Field.STARTED]

    status: List[Status] = attribute(factory=lambda: GetAssignmentsTsvParameters._default_status)
    start_time_from: Optional[datetime.datetime] = attribute(origin='startTimeFrom')
    start_time_to: Optional[datetime.datetime] = attribute(origin='startTimeTo')
    exclude_banned: Optional[bool] = attribute(origin='excludeBanned')
    field: List[Field] = attribute(
        factory=lambda: GetAssignmentsTsvParameters._default_fields
    )

    @classmethod
    def structure(cls, data):
        raise NotImplementedError

    def unstructure(self) -> dict:
        data = super().unstructure()
        data['status'] = ','.join(data['status'])
        data['field'] = ','.join(data['field'])
        data['addRowDelimiter'] = False
        return data
