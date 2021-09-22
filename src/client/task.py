__all__ = [
    'BaseTask',
    'Task',
    'CreateTaskParameters',
    'CreateTaskAsyncParameters',
    'CreateTasksParameters',
    'TaskOverlapPatch',
    'TaskPatch'
]
import datetime
from typing import Any, Dict, List
from uuid import UUID

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters
from ..util._codegen import attribute
from ..util._docstrings import inherit_docstrings


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

        output_values: Dict[str, Any]
        correctness_weight: float

    input_values: Dict[str, Any]
    known_solutions: List[KnownSolution]
    message_on_unknown_solution: str

    # Readonly
    id: str = attribute(readonly=True)
    origin_task_id: str = attribute(readonly=True)


@inherit_docstrings
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
        ...
    """

    class BaselineSolution(BaseTolokaObject):
        output_values: Dict[str, Any]
        confidence_weight: float

    pool_id: str

    remaining_overlap: int = attribute(readonly=True)
    reserved_for: List[str]
    unavailable_for: List[str]
    traits_all_of: List[str]
    traits_any_of: List[str]
    traits_none_of_any: List[str]
    origin_task_id: str = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)
    baseline_solutions: List[BaselineSolution]


class CreateTaskParameters(Parameters):
    """Parameters for Task creation controlling

    Used when creating one Task.

    Attributes:
        allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).
            * False - Use the overlap that is set in the task suite parameters (in the overlap field).
        open_pool: Open the pool immediately after creating a task suite, if the pool is closed.
    """

    allow_defaults: bool
    open_pool: bool


@inherit_docstrings
class CreateTaskAsyncParameters(CreateTaskParameters):
    operation_id: UUID


@inherit_docstrings
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

    skip_invalid_items: bool
    operation_id: UUID
    async_mode: bool = attribute(default=True)


class TaskOverlapPatch(BaseTolokaObject):
    """Parameters for changing the overlap of a specific Task

    Attributes:
        overlap: Overlapping a set of tasks.
        infinite_overlap: Issue a task with infinite overlap. Used, for example, for sets of training tasks to give them to all users:
            * True - Set infinite overlap.
            * False - Leave the overlap specified for the task or pool. Default Behaviour.
    """

    overlap: int
    infinite_overlap: bool


@inherit_docstrings
class TaskPatch(TaskOverlapPatch):
    """Parameters for changing overlap or baseline_solutions of a specific Task

    Attributes:
        baseline_solutions:
    """

    baseline_solutions: List[Task.BaselineSolution]
