from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters


class BaseTask(BaseTolokaObject):
    """Base class for Task

    Attributes:
        input_values: Input data for a task. List of pairs:
            "<output field ID 1>": "<field value 1>",
            "<output field ID 1>": "<field value 2>",
            ...
            "<output field ID n>": "<field value n>"
        known_solutions: Responses and hints for control tasks and training tasks.
            If multiple output fields are included in the validation, all combinations of the correct response
            must be specified.
        message_on_unknown_solution: Hint for the task (for training tasks).
        id: Task ID.
        origin_task_id: ID of the task it was copied from
    """

    class KnownSolution(BaseTolokaObject):

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
            output_values: Optional[Dict[str, Any]] = ...,
            correctness_weight: Optional[float] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        output_values: Optional[Dict[str, Any]]
        correctness_weight: Optional[float]

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
        input_values: Optional[Dict[str, Any]] = ...,
        known_solutions: Optional[List[KnownSolution]] = ...,
        message_on_unknown_solution: Optional[str] = ...,
        id: Optional[str] = ...,
        origin_task_id: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    input_values: Optional[Dict[str, Any]]
    known_solutions: Optional[List[KnownSolution]]
    message_on_unknown_solution: Optional[str]
    id: Optional[str]
    origin_task_id: Optional[str]

class Task(InfiniteOverlapParametersMixin, BaseTask):
    """Task

    Attributes:
        pool_id: The ID of the pool that the task is uploaded to.
        remaining_overlap: Optional[int]
        reserved_for: IDs of users who will have access to the task.
        unavailable_for: IDs of users who shouldn't have access to the task.
        traits_all_of: Optional[List[str]]
        traits_any_of: Optional[List[str]]
        traits_none_of_any: Optional[List[str]]
        origin_task_id: ID of the task it was copied from
        created: The UTC date and time when the task suite was created
        baseline_solutions: Optional[List[BaselineSolution]]
    """

    class BaselineSolution(BaseTolokaObject):

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
            output_values: Optional[Dict[str, Any]] = ...,
            confidence_weight: Optional[float] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        output_values: Optional[Dict[str, Any]]
        confidence_weight: Optional[float]

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
        input_values: Optional[Dict[str, Any]] = ...,
        known_solutions: Optional[List[BaseTask.KnownSolution]] = ...,
        message_on_unknown_solution: Optional[str] = ...,
        id: Optional[str] = ...,
        infinite_overlap=...,
        overlap=...,
        pool_id: Optional[str] = ...,
        remaining_overlap: Optional[int] = ...,
        reserved_for: Optional[List[str]] = ...,
        unavailable_for: Optional[List[str]] = ...,
        traits_all_of: Optional[List[str]] = ...,
        traits_any_of: Optional[List[str]] = ...,
        traits_none_of_any: Optional[List[str]] = ...,
        origin_task_id: Optional[str] = ...,
        created: Optional[datetime] = ...,
        baseline_solutions: Optional[List[BaselineSolution]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    input_values: Optional[Dict[str, Any]]
    known_solutions: Optional[List[BaseTask.KnownSolution]]
    message_on_unknown_solution: Optional[str]
    id: Optional[str]
    pool_id: Optional[str]
    remaining_overlap: Optional[int]
    reserved_for: Optional[List[str]]
    unavailable_for: Optional[List[str]]
    traits_all_of: Optional[List[str]]
    traits_any_of: Optional[List[str]]
    traits_none_of_any: Optional[List[str]]
    origin_task_id: Optional[str]
    created: Optional[datetime]
    baseline_solutions: Optional[List[BaselineSolution]]

class CreateTaskParameters(Parameters):
    """CreateTaskParameters

    Attributes:
        allow_defaults: Overlap settings:
            * True — Use the overlap that is set in the pool parameters (in the
                defaults.default_overlap_for_new_task_suites key).
            * False — Use the overlap that is set in the task suite parameters (in the overlap field).
        open_pool: Open the pool immediately after creating a task suite, if the pool is closed.
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
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]

class CreateTaskAsyncParameters(CreateTaskParameters):

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
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        operation_id: Optional[UUID] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]
    operation_id: Optional[UUID]

class CreateTasksParameters(CreateTaskParameters):
    """CreateTasksParameters

    Attributes:
        allow_defaults: Overlap settings:
            * True — Use the overlap that is set in the pool parametersß.
            * False — Use the overlap that is set in the task parameters (in the overlap field).
        open_pool: Open the pool immediately after creating a task, if the pool is closed.
        skip_invalid_items: Validation parameters:
            * True — Create the tasks that passed validation. Skip the rest of the tasks (errors will
                be listed in the response to the request).
            * False — If at least one of the tasks didn't pass validation, stop the operation and don't create any tasks.
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
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        skip_invalid_items: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]
    skip_invalid_items: Optional[bool]

class CreateTasksAsyncParameters(CreateTasksParameters):
    """CreateTasksAsyncParameters

    Attributes:
        allow_defaults: Overlap settings:
            * True — Use the overlap that is set in the pool parametersß.
            * False — Use the overlap that is set in the task parameters (in the overlap field).
        open_pool: Open the pool immediately after creating a task, if the pool is closed.
        skip_invalid_items: Validation parameters:
            * True — Create the tasks that passed validation. Skip the rest of the tasks (errors will
                be listed in the response to the request).
            * False — If at least one of the tasks didn't pass validation, stop the operation and don't create any tasks.
        operation_id: Operation ID for asynchronous loading of tasks.
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
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...,
        skip_invalid_items: Optional[bool] = ...,
        operation_id: Optional[UUID] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]
    skip_invalid_items: Optional[bool]
    operation_id: Optional[UUID]

class TaskOverlapPatch(BaseTolokaObject):

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
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    overlap: Optional[int]
    infinite_overlap: Optional[bool]

class TaskPatch(TaskOverlapPatch):

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
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...,
        baseline_solutions: Optional[List[Task.BaselineSolution]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    overlap: Optional[int]
    infinite_overlap: Optional[bool]
    baseline_solutions: Optional[List[Task.BaselineSolution]]
