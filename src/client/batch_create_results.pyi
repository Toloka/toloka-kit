from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus


class FieldValidationError(BaseTolokaObject):

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
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        params: Optional[List[Any]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    code: Optional[str]
    message: Optional[str]
    params: Optional[List[Any]]

class TaskBatchCreateResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, Task]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]

class TaskSuiteBatchCreateResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, TaskSuite]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]

class UserBonusBatchCreateResult(BaseTolokaObject):

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, UserBonus]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]
