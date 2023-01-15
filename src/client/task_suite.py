__all__ = [
    'TaskSuite',
    'TaskSuiteCreateRequestParameters',
    'TaskSuiteOverlapPatch',
    'TaskSuitePatch'
]
import datetime
from typing import List
from uuid import UUID

import attr

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters
from .task import BaseTask
from ..util._codegen import attribute, expand


class TaskSuite(InfiniteOverlapParametersMixin, BaseTolokaObject):
    """A set of tasks assigned to a Toloker at once.

    A task suite contains one or more tasks. Tolokers are paid after completing all tasks in a task suite.

    Attributes:
        pool_id: The ID of a pool that the task suite belongs to.
        tasks: The tasks.
        reserved_for: IDs of Tolokers who have access to the task suite.
        unavailable_for: IDs of Tolokers who don't have access to the task suite.
        issuing_order_override: The priority of a task suite.
            It influences the order of assigning task suites to Tolokers in pools with the `issue_task_suites_in_creation_order` parameter set to `True`.
            Allowed range: from -99999.99999 to 99999.99999.
        mixed: [The way of grouping tasks](https://toloka.ai/en/docs/guide/concepts/distribute-tasks-by-pages) to create the task suite.
            * True — The tasks are mixed automatically using the smart mixing approach.
            * False — The tasks are grouped manually.

            Default value: `False`.
        traits_all_of: The task suite can be assigned to Tolokers who have all of the specified traits.
        traits_any_of: The task suite can be assigned to Tolokers who have any of the specified traits.
        traits_none_of_any: The task suite can not be assigned to Tolokers who have any of the specified traits.
        longitude: The longitude of the point on the map for the task suite.
        latitude: The latitude of the point on the map for the task suite.
        id: The ID of the task suite. This parameter is read only.
        remaining_overlap: The number of times left for this task suite to be assigned to Tolokers. This parameter is read only.
        automerged:
            * True — The task suite was created after [merging tasks](https://toloka.ai/en/docs/api/concepts/tasks#task-merge).
            * False — There are no merged tasks in the task suite.
        created: The UTC date and time when the task suite was created. This parameter is read only.
    """

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
    id: str = attribute(readonly=True)
    remaining_overlap: int = attribute(readonly=True)
    automerged: bool = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)

    @expand('base_task')
    def add_base_task(self, base_task: BaseTask) -> 'TaskSuite':
        self.tasks.append(base_task)
        return self


class TaskSuiteCreateRequestParameters(Parameters):
    """Parameters for creating task suites.

    Attributes:
        operation_id: The ID of the operation conforming to the [RFC4122 standard](https://tools.ietf.org/html/rfc4122). Use it if the `async_mode` is set to `True`.
        skip_invalid_items: Task suite validation option:
            * True — All valid task suites are added. If a task suite does not pass validation, then it is not added to Toloka.
            * False — If any task suite does not pass validation, then operation is cancelled and no task suites are added to Toloka.

            Default value: `False`.
        allow_defaults: Active overlap setting:
            * True — Use the overlap that is set in the `defaults.default_overlap_for_new_task_suites` pool parameter.
            * False — Use the overlap that is set in the `overlap` task suite parameter.

            Default value: `False`.
        open_pool: Open the pool immediately after creating a task suite, if the pool is closed.
        async_mode: Request processing mode:
            * True — Asynchronous operation is started internally.
            * False — The request is processed synchronously. A maximum of 5000 task suites can be added in a single request in this mode.

            Default value: `True`.
    """

    operation_id: UUID
    skip_invalid_items: bool
    allow_defaults: bool
    open_pool: bool
    async_mode: bool = attribute(default=True)


class TaskSuiteOverlapPatch(BaseTolokaObject):
    """Parameters for stopping assigning a task suite.

    Attributes:
        overlap: The new overlap value.
    """

    overlap: int


class TaskSuitePatch(InfiniteOverlapParametersMixin, BaseTolokaObject):
    """Parameters for changing a task suite.

    Attributes:
        issuing_order_override: The priority of a task suite.
            It influences the order of assigning task suites to Tolokers in pools with the `issue_task_suites_in_creation_order` parameter set to `True`.
            Allowed range: from -99999.99999 to 99999.99999. Default value: 0.
        open_pool: Open the pool immediately after changing a task suite, if the pool is closed.

            Default value: `False`.
    """

    issuing_order_override: float
    open_pool: bool
