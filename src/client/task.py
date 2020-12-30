import datetime
from typing import Any, Dict, List
from uuid import UUID

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters


class BaseTask(BaseTolokaObject):

    class KnownSolution(BaseTolokaObject):
        output_values: Dict[str, Any]
        correctness_weight: float

    input_values: Dict[str, Any]
    known_solutions: List[KnownSolution]
    message_on_unknown_solution: str

    # Readonly
    id: str
    origin_task_id: str


class Task(InfiniteOverlapParametersMixin, BaseTask):

    class BaselineSolution(BaseTolokaObject):
        output_values: Dict[str, Any]
        confidence_weight: float

    pool_id: str

    remaining_overlap: int
    reserved_for: List[str]
    unavailable_for: List[str]
    traits_all_of: List[str]
    traits_any_of: List[str]
    traits_none_of_any: List[str]
    origin_task_id: str
    created: datetime.datetime
    baseline_solutions: List[BaselineSolution]


class CreateTaskParameters(Parameters):
    allow_defaults: bool
    open_pool: bool


class CreateTaskAsyncParameters(CreateTaskParameters):
    operation_id: UUID


class CreateTasksParameters(CreateTaskParameters):
    skip_invalid_items: bool


class CreateTasksAsyncParameters(CreateTasksParameters):
    operation_id: UUID


class TaskOverlapPatch(BaseTolokaObject):
    overlap: int
    infinite_overlap: bool


class TaskPatch(TaskOverlapPatch):
    baseline_solutions: List[Task.BaselineSolution]
