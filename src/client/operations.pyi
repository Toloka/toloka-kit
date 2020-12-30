from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class OperationType(Enum):
    ...

class Operation(BaseTolokaObject):
    """Tracking Operation

    Some API requests (opening and closing a pool, archiving a pool or a project, loading multiple tasks,
    awarding bonuses) are processed as asynchronous operations that run in the background.
    Attributes:
        id: Operation ID.
        status: The status of the operation.
        submitted: The UTC date and time the request was sent.
        parameters: Operation parameters (depending on the operation type).
        started: The UTC date and time the operation started.
        finished: The UTC date and time the operation finished.
        progress: The percentage of the operation completed.
        details: Details of the operation completion.
    """

    class Status(Enum):
        """The status of the operation:

        * PENDING — Not started yet.
        * RUNNING — In progress.
        * SUCCESS — Completed successfully.
        * FAIL — Not completed.
        """
        ...

    class Parameters(BaseTolokaObject):
        """Operation parameters (depending on the operation type).

        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self) -> None: ...

        _unexpected: Optional[Dict[str, Any]]

    def is_completed(self): ...

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
        id: Optional[str] = ...,
        status: Optional[Status] = ...,
        submitted: Optional[datetime] = ...,
        parameters: Optional[Parameters] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Status]
    submitted: Optional[datetime]
    parameters: Optional[Parameters]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]

class PoolOperation(Operation):

    class Parameters(Operation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, pool_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[Parameters]

class PoolArchiveOperation(PoolOperation):

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[PoolOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[PoolOperation.Parameters]

class PoolCloneOperation(PoolOperation):

    class Details(PoolOperation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, pool_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        parameters: Optional[PoolOperation.Parameters] = ...,
        details: Optional[Details] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    parameters: Optional[PoolOperation.Parameters]
    details: Optional[Details]

class PoolCloseOperation(PoolOperation):

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[PoolOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[PoolOperation.Parameters]

class PoolOpenOperation(PoolOperation):

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[PoolOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[PoolOperation.Parameters]

class ProjectArchiveOperation(Operation):

    class Parameters(Operation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, project_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        project_id: Optional[str]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[Parameters]

class TasksCreateOperation(Operation):
    """TasksCreateOperation

    Attributes:
        parameters: Parameters
        finished: The UTC date and time the operation was completed.
        details: Any
    """

    class Parameters(Operation.Parameters):
        """Parameters

        Attributes:
            skip_invalid_items: Validation parameters for JSON objects:
                * True — Create the tasks that passed validation. Skip the rest of the tasks.
                * False — If at least one of the tasks didn't pass validation, stop the operation and
                    don't create any tasks.
            allow_defaults: Overlap settings:
                * True — Use the overlap that is set in the pool parameters
                    (in the defaults.default_overlap_for_new_tasks key).
                * False — Use the overlap that is set in the task parameters (in the overlap field).
            open_pool: Open the pool immediately after creating the tasks, if the pool is closed.
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
            skip_invalid_items: Optional[bool] = ...,
            allow_defaults: Optional[bool] = ...,
            open_pool: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skip_invalid_items: Optional[bool]
        allow_defaults: Optional[bool]
        open_pool: Optional[bool]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        parameters: Optional[Parameters] = ...,
        finished: Optional[datetime] = ...,
        details: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    progress: Optional[int]
    parameters: Optional[Parameters]
    finished: Optional[datetime]
    details: Optional[Any]

class TaskSuiteCreateBatchOperation(Operation):

    class Parameters(Operation.Parameters):

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
            skip_invalid_items: Optional[bool] = ...,
            allow_defaults: Optional[bool] = ...,
            open_pool: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skip_invalid_items: Optional[bool]
        allow_defaults: Optional[bool]
        open_pool: Optional[bool]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        parameters: Optional[Parameters] = ...,
        finished: Optional[datetime] = ...,
        details: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    progress: Optional[int]
    parameters: Optional[Parameters]
    finished: Optional[datetime]
    details: Optional[Any]

class AggregatedSolutionOperation(Operation):

    class Parameters(Operation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, pool_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[Parameters]

class UserBonusCreateBatchOperation(Operation):

    class Parameters(Operation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, skip_invalid_items: Optional[bool] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skip_invalid_items: Optional[bool]

    class Details(PoolOperation.Parameters):

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
            pool_id: Optional[str] = ...,
            total_count: Optional[int] = ...,
            valid_count: Optional[int] = ...,
            not_valid_count: Optional[int] = ...,
            success_count: Optional[int] = ...,
            failed_count: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]
        total_count: Optional[int]
        valid_count: Optional[int]
        not_valid_count: Optional[int]
        success_count: Optional[int]
        failed_count: Optional[int]

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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        parameters: Optional[Parameters] = ...,
        details: Optional[Details] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    parameters: Optional[Parameters]
    details: Optional[Details]
