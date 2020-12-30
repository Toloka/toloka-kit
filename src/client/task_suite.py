import datetime
from typing import List
from uuid import UUID

import attr

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters
from .task import BaseTask
from .util._codegen import expand


class TaskSuite(InfiniteOverlapParametersMixin, BaseTolokaObject):
    pool_id: str
    tasks: List[BaseTask] = attr.attrib(factory=list)

    reserved_for: List[str]
    unavailable_for: List[str]
    issuing_order_override: float
    mixed: bool

    traits_all_of: List[str]
    traits_any_of: List[str]
    traits_none_of_any: List[str]

    longitude: float
    latitude: float

    # Readonly
    id: str
    remaining_overlap: int
    automerged: bool
    created: datetime.datetime

    @expand('base_task')
    def add_base_task(self, base_task: BaseTask) -> 'TaskSuite':
        self.tasks.append(base_task)
        return self


class TaskSuiteCreateRequestParameters(Parameters):
    operation_id: UUID
    skip_invalid_items: bool
    allow_defaults: bool
    open_pool: bool


class TaskSuiteOverlapPatch(BaseTolokaObject):
    overlap: int


class TaskSuitePatch(InfiniteOverlapParametersMixin, BaseTolokaObject):
    issuing_order_override: float
    open_pool: bool
