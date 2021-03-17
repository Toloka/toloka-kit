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
            "<input field ID 1>": "<field value 1>",
            "<input field ID 1>": "<field value 2>",
            ...
            "<input field ID n>": "<field value n>"
        known_solutions: Responses and hints for control tasks and training tasks. If multiple output fields are included
            in the validation, all combinations of the correct response must be specified.
        message_on_unknown_solution: Hint for the task (for training tasks).
        id: Task ID.
        origin_task_id: ID of the task it was copied from.
    """

    class KnownSolution(BaseTolokaObject):
        """Answers and hints for control and training tasks.

        If several output fields are taken into account when checking, you must specify all combinations of the correct answer.

        Attributes:
            output_values: Correct answers in the task (for control tasks). If there are several correct answer options,
                for each option you need to define output_values and give the weight of the correct answer (key correctness_weight).
                "<output field id 1>": "<correct answer value 1>",
                "<output field id 2>": "<correct answer value 2>",
                ...
                "<output field id n>": "<correct answer value n>"
            correctness_weight: Weight of the correct answer. Allows you to set several options for correct answers and
                rank them by correctness. For example, if the weight of the correct answer is 0.5, half of the error is
                counted to the user. The more correct the answer in correctValues, the higher its weight.
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
    """The task that will be issued to the performers

    Not to be confused with TaskSuite - a set of tasks that is shown to the user at one time.
    TaskSuite may contain several Tasks.

    Attributes:
        pool_id: The ID of the pool that the task is uploaded to.
        reserved_for: IDs of users who will have access to the task.
        unavailable_for: IDs of users who shouldn't have access to the task.
        traits_all_of:
        traits_any_of:
        traits_none_of_any:
        created: The UTC date and time when the task was created.
        baseline_solutions:
        remaining_overlap: How many times will this task be issued to performers. Read Only field.

    Example:
        How to create tasks.

        >>> tasks = [
        >>>     Task(input_values={'image': 'https://some.url/my_img0001.png'}, pool_id=my_pool_id),
        >>>     Task(input_values={'image': 'https://some.url/my_img0002.png'}, pool_id=my_pool_id),
        >>> ]
        >>> created_tasks = toloka_client.create_tasks(tasks, allow_defaults=True)
        >>> print(len(created_tasks.items))
        2
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
    """Parameters for Task creation controlling

    Used when creating one Task.

    Attributes:
        allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).
            * False - Use the overlap that is set in the task suite parameters (in the overlap field).
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
    """Parameters for Tasks creation controlling

    Used when creating many Tasks.

    Attributes:
        skip_invalid_items: Validation parameters:
            * True — Create the tasks that passed validation. Skip the rest of the tasks (errors will
                be listed in the response to the request).
            * False — If at least one of the tasks didn't pass validation, stop the operation and don't create any tasks.
        async_mode: How the request is processed:
            * True — deferred. The query results in an asynchronous operation running in the background.
                The response contains information about the operation (start and end time, status, number of sets).
            * False — synchronous. The response contains information about the created tasks.
                A maximum of 5000 tasks can be sent in a single request.
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
        operation_id: Optional[UUID] = ...,
        async_mode: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]
    skip_invalid_items: Optional[bool]
    operation_id: Optional[UUID]
    async_mode: Optional[bool]

class TaskOverlapPatch(BaseTolokaObject):
    """Parameters for changing the overlap of a specific Task

    Attributes:
        overlap: Overlapping a set of tasks.
        infinite_overlap: Issue a task with infinite overlap. Used, for example, for sets of training tasks to give them to all users:
            * True - Set infinite overlap.
            * False - Leave the overlap specified for the task or pool. Default Behaviour.
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
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    overlap: Optional[int]
    infinite_overlap: Optional[bool]

class TaskPatch(TaskOverlapPatch):
    """Parameters for changing overlap or baseline_solutions of a specific Task

    Attributes:
        baseline_solutions:
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
        overlap: Optional[int] = ...,
        infinite_overlap: Optional[bool] = ...,
        baseline_solutions: Optional[List[Task.BaselineSolution]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    overlap: Optional[int]
    infinite_overlap: Optional[bool]
    baseline_solutions: Optional[List[Task.BaselineSolution]]
