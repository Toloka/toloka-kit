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
    public_comment: str
    status: Assignment.Status


class GetAssignmentsTsvParameters(Parameters):

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
