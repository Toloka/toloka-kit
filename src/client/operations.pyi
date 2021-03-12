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

        * PENDING - Not started yet.
        * RUNNING - In progress.
        * SUCCESS - Completed successfully.
        * FAIL - Not completed.
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

class AnalyticsOperation(Operation):
    """Operation returned when requesting analytics via TolokaClient.get_analytics()
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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        parameters: Optional[Operation.Parameters] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    parameters: Optional[Operation.Parameters]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]

class PoolOperation(Operation):
    """Base class for all operations on pool

    Attributes:
        parameters.pool_id: On which pool operation is performed.
    """

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
    """Operation returned by an asynchronous archive pool via TolokaClient.archive_pool_async()
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
    """Operation returned by an asynchronous cloning pool via TolokaClient.clone_pool_async()

    As parameters.pool_id contains id of the pool that needs to be cloned.
    New pool id stored in details.pool_id.
    Don't be mistaken.

    Attributes:
        details.pool_id: New pool id created after cloning.
    """

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
    """Operation returned by an asynchronous closing pool via TolokaClient.close_pool_async()
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
    """Operation returned by an asynchronous opening pool via TolokaClient.open_pool_async()
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

class TrainingOperation(Operation):
    """Base class for all operations on training pool

    Attributes:
        parameters.training_id: On which training pool operation is performed.
    """

    class Parameters(Operation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, training_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        training_id: Optional[str]

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

class TrainingArchiveOperation(TrainingOperation):
    """Operation returned by an asynchronous archive training pool via TolokaClient.archive_training_async()
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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[TrainingOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[TrainingOperation.Parameters]

class TrainingCloneOperation(TrainingOperation):
    """Operation returned by an asynchronous cloning training pool via TolokaClient.clone_training_async()

    As parameters.training_id contains id of the training pool that needs to be cloned.
    New training pool id stored in details.training_id.
    Don't be mistaken.

    Attributes:
        details.pool_id: New training pool id created after cloning.
    """

    class Details(TrainingOperation.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, training_id: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        training_id: Optional[str]

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
        parameters: Optional[TrainingOperation.Parameters] = ...,
        details: Optional[Details] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    parameters: Optional[TrainingOperation.Parameters]
    details: Optional[Details]

class TrainingCloseOperation(TrainingOperation):
    """Operation returned by an asynchronous closing training pool via TolokaClient.close_training_async()
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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[TrainingOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[TrainingOperation.Parameters]

class TrainingOpenOperation(TrainingOperation):
    """Operation returned by an asynchronous opening training pool via TolokaClient.open_training_async()
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
        id: Optional[str] = ...,
        status: Optional[Operation.Status] = ...,
        submitted: Optional[datetime] = ...,
        started: Optional[datetime] = ...,
        finished: Optional[datetime] = ...,
        progress: Optional[int] = ...,
        details: Optional[Any] = ...,
        parameters: Optional[TrainingOperation.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    status: Optional[Operation.Status]
    submitted: Optional[datetime]
    started: Optional[datetime]
    finished: Optional[datetime]
    progress: Optional[int]
    details: Optional[Any]
    parameters: Optional[TrainingOperation.Parameters]

class ProjectArchiveOperation(Operation):
    """Operation returned by an asynchronous archive project via TolokaClient.archive_project_async()

    Attributes:
        parameters.project_id: On which project operation is performed.
    """

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
    """Operation returned by an asynchronous creating tasks via TolokaClient.create_tasks_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the tasks that passed validation. Skip the rest of the tasks.
            * False - If at least one of the tasks didn't pass validation, stop the operation and
                don't create any tasks.
        parameters.allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters
                (in the defaults.default_overlap_for_new_tasks key).
            * False - Use the overlap that is set in the task parameters (in the overlap field).
        parameters.open_pool: Open the pool immediately after creating the tasks, if the pool is closed.
    """

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

class TaskSuiteCreateBatchOperation(Operation):
    """Operation returned by an asynchronous creating TaskSuite's via TolokaClient.create_task_suites_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the task suites that passed validation. Skip the rest of the task suites.
            * False - If at least one of the task suites didn't pass validation, stop the operation and
                don't create any task suites.
        parameters.allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters.
            * False - Use the overlap that is set in the task parameters (in the overlap field).
        parameters.open_pool: Open the pool immediately after creating the task suites, if the pool is closed.
    """

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
    """Operation returned by an asynchronous aggregation responses in pool via TolokaClient.aggregate_solutions_by_pool()

    Attributes:
        parameters.pool_id: In which pool the responses are aggregated.
    """

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
    """Operation returned by an asynchronous creating user bonuses via TolokaClient.create_user_bonuses_async()

    All parameters are for reference only and describe the initial parameters of the request that this operation monitors.

    Attributes:
        parameters.skip_invalid_items: Validation parameters for JSON objects:
            * True - Create the user bonuses that passed validation. Skip the rest of the user bonuses.
            * False - If at least one of the user bonus didn't pass validation, stop the operation and
                don't create any user bonus.
        details.pool_id:
        details.total_count: The number of bonuses in the request.
        details.valid_count: The number of JSON objects with bonus information that have passed validation.
        details.not_valid_count: The number of JSON objects with bonus information that failed validation.
        details.success_count: Number of bonuses issued.
        details.failed_count: The number of bonuses that were not issued.
    """

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
