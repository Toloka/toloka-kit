from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject
from .task import Task
from .task_suite import TaskSuite
from .user_bonus import UserBonus


class FieldValidationError(BaseTolokaObject):
    """Error that contains information about an invalid field

    Attributes:
        code: error code string.
        message: error message.
        params: additional params.
    """

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
    """The list with the results of the tasks creation operation.

    Attributes:
        items: Object with created tasks.
        validation_errors: Object with errors in tasks. Returned if the parameter is used in the request skip_invalid_items=True.
    """

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, Task]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]

class TaskSuiteBatchCreateResult(BaseTolokaObject):
    """The list with the results of the task suites creation operation.

    Attributes:
        items: Object with created task suites.
        validation_errors: Object with errors in task suites. Returned if the parameter is used in the request skip_invalid_items=True.
    """

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, TaskSuite]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]

class UserBonusBatchCreateResult(BaseTolokaObject):
    UserBonus,
    """The list with the results of the user bonuses creation operation.

    Attributes:
        items: Object with information about issued bonuses.
        validation_errors: Object with validation errors. Returned if the parameter is used in the request skip_invalid_items=True.
    """

    _unexpected: Optional[Dict[str, Any]]
    items: Optional[Dict[str, UserBonus]]
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]]
