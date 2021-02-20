from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .owner import Owner
from .primitives.base import BaseTolokaObject


class Training(BaseTolokaObject):

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
        inherited_instructions: Optional[str] = ...,
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
    inherited_instructions: Optional[str]
    public_instructions: Optional[str]
    metadata: Optional[Dict[str, List[str]]]
    owner: Optional[Owner]
    id: Optional[str]
    status: Optional[Status]
    last_close_reason: Optional[CloseReason]
    created: Optional[datetime]
    last_started: Optional[datetime]
    last_stopped: Optional[datetime]
