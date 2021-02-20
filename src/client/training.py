import datetime
from enum import Enum, unique
from typing import Dict, List

from .owner import Owner
from .primitives.base import BaseTolokaObject
from .util._codegen import codegen_attr_attributes_setters


@codegen_attr_attributes_setters
class Training(BaseTolokaObject):

    @unique
    class CloseReason(Enum):
        MANUAL = 'MANUAL'
        EXPIRED = 'EXPIRED'
        COMPLETED = 'COMPLETED'
        NOT_ENOUGH_BALANCE = 'NOT_ENOUGH_BALANCE'
        ASSIGNMENTS_LIMIT_EXCEEDED = 'ASSIGNMENTS_LIMIT_EXCEEDED'
        BLOCKED = 'BLOCKED'
        FOR_UPDATE = 'FOR_UPDATE'

    @unique
    class Status(Enum):
        OPEN = 'OPEN'
        CLOSED = 'CLOSED'
        ARCHIVED = 'ARCHIVED'
        LOCKED = 'LOCKED'

    project_id: str
    private_name: str
    may_contain_adult_content: bool
    assignment_max_duration_seconds: int
    mix_tasks_in_creation_order: bool
    shuffle_tasks_in_task_suite: bool
    training_tasks_in_task_suite_count: int
    task_suites_required_to_pass: int
    retry_training_after_days: int
    inherited_instructions: bool
    public_instructions: str

    metadata: Dict[str, List[str]]
    owner: Owner

    # Readonly
    id: str
    status: Status
    last_close_reason: CloseReason
    created: datetime.datetime
    last_started: datetime.datetime
    last_stopped: datetime.datetime

    def is_open(self) -> bool:
        return self.status == Training.Status.OPEN

    def is_closed(self) -> bool:
        return self.status == Training.Status.CLOSED

    def is_archived(self) -> bool:
        return self.status == Training.Status.ARCHIVED

    def is_locked(self) -> bool:
        return self.status == Training.Status.LOCKED
