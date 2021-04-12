__all__ = ['Training']
import datetime
from enum import Enum, unique
from typing import Dict, List

from .owner import Owner
from .primitives.base import BaseTolokaObject
from .util._codegen import codegen_attr_attributes_setters


@codegen_attr_attributes_setters
class Training(BaseTolokaObject):
    """Training pool

    Allows:
     - Select for the main pool only those performers who successfully complete the training tasks.
     - Practice performers before the main pool and figure out how to respond correctly.

    Attributes:
        project_id: ID of the project to which the training pool belongs.
        private_name: Training pool name (only visible to the requester).
        may_contain_adult_content: The presence of adult content in learning tasks.
        assignment_max_duration_seconds: Time to complete a set of tasks in seconds.
            It is recommended to allocate at least 60 seconds for a set of tasks
            (taking into account the time for loading the page, sending responses).
        mix_tasks_in_creation_order: The order in which tasks are included in sets:
            * True - Default Behaviour. Include tasks in sets in the order they were loaded.
            * False - Include tasks in sets in random order.
        shuffle_tasks_in_task_suite: Order of tasks within the task set:
            * true - Random. Default Behaviour.
            * false - The order in which the tasks were loaded.
        training_tasks_in_task_suite_count: The number of tasks in the set.
        task_suites_required_to_pass: The number of task suites that must be successfully completed to assign a skill
            and access the main tasks.
        retry_training_after_days: After how many days the replay will become available.
        inherited_instructions: Indicates whether to use a project statement.
            If training need their own instruction, then specify it in public_instructions. Default value - False.
        public_instructions: Instructions for completing training tasks. May contain HTML markup.
        metadata:
        owner: Training pool owner.
        id: Internal ID of the training pool. Read only.
        status: Training pool status. Read only.
        last_close_reason: The reason the training pool was last closed.
        created: UTC date and time of creation of the training pool in ISO 8601 format. Read only.
        last_started: UTC date and time of the last start of the training pool in ISO 8601 format. Read only.
        last_stopped: UTC date and time of the last stop of the training pool in ISO 8601 format. Read only.
    """

    @unique
    class CloseReason(Enum):
        """The reason for closing the pool the last time:

        Attributes:
            MANUAL: Closed by the requester.
            EXPIRED: Reached the date and time set in will_expire.
            COMPLETED: Closed automatically because all the pool tasks were completed.
            NOT_ENOUGH_BALANCE: Closed automatically because the Toloka account ran out of funds.
            ASSIGNMENTS_LIMIT_EXCEEDED: Closed automatically because it exceeded the limit on assigned task suites
                (maximum of 2 million).
            BLOCKED: Closed automatically because the requester's account was blocked by a Toloka administrator.
        """
        MANUAL = 'MANUAL'
        EXPIRED = 'EXPIRED'
        COMPLETED = 'COMPLETED'
        NOT_ENOUGH_BALANCE = 'NOT_ENOUGH_BALANCE'
        ASSIGNMENTS_LIMIT_EXCEEDED = 'ASSIGNMENTS_LIMIT_EXCEEDED'
        BLOCKED = 'BLOCKED'
        FOR_UPDATE = 'FOR_UPDATE'

    @unique
    class Status(Enum):
        """Status of the training pool

        Attributes:
            OPEN: Training pool is open
            CLOSED: Training pool is closed
            ARCHIVED: Training pool is archived
            LOCKED: Training pool is locked
        """
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
