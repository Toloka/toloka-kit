from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .owner import Owner
from .primitives.base import BaseTolokaObject


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

    class CloseReason(Enum):
        ...

    class Status(Enum):
        ...

    def is_open(self) -> bool: ...

    def is_closed(self) -> bool: ...

    def is_archived(self) -> bool: ...

    def is_locked(self) -> bool: ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        project_id: Optional[str] = ...,
        private_name: Optional[str] = ...,
        may_contain_adult_content: Optional[bool] = ...,
        assignment_max_duration_seconds: Optional[int] = ...,
        mix_tasks_in_creation_order: Optional[bool] = ...,
        shuffle_tasks_in_task_suite: Optional[bool] = ...,
        training_tasks_in_task_suite_count: Optional[int] = ...,
        task_suites_required_to_pass: Optional[int] = ...,
        retry_training_after_days: Optional[int] = ...,
        inherited_instructions: Optional[bool] = ...,
        public_instructions: Optional[str] = ...,
        metadata: Optional[Dict[str, List[str]]] = ...,
        owner: Optional[Owner] = ...,
        id: Optional[str] = ...,
        status: Optional[Status] = ...,
        last_close_reason: Optional[CloseReason] = ...,
        created: Optional[datetime] = ...,
        last_started: Optional[datetime] = ...,
        last_stopped: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    project_id: Optional[str]
    private_name: Optional[str]
    may_contain_adult_content: Optional[bool]
    assignment_max_duration_seconds: Optional[int]
    mix_tasks_in_creation_order: Optional[bool]
    shuffle_tasks_in_task_suite: Optional[bool]
    training_tasks_in_task_suite_count: Optional[int]
    task_suites_required_to_pass: Optional[int]
    retry_training_after_days: Optional[int]
    inherited_instructions: Optional[bool]
    public_instructions: Optional[str]
    metadata: Optional[Dict[str, List[str]]]
    owner: Optional[Owner]
    id: Optional[str]
    status: Optional[Status]
    last_close_reason: Optional[CloseReason]
    created: Optional[datetime]
    last_started: Optional[datetime]
    last_stopped: Optional[datetime]
