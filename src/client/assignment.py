from attr.validators import optional, instance_of
import datetime
from decimal import Decimal
from enum import Enum, unique
from typing import List

from .primitives.base import attribute, BaseTolokaObject
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
