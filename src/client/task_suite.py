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
    """A set of tasks issued to the Toloker at a time

    TaskSuite can contain one or more tasks. The execution price is charged for one TaskSuite.
    Tolokers receive exactly one TaskSuite when they take on your task.

    Attributes:
        pool_id: The ID of the pool that task suite are uploaded to.
        tasks: Data for the tasks.
        reserved_for: IDs of Tolokers who will have access to the task suite.
        unavailable_for: IDs of Tolokers who shouldn't have access to the task suite.
        issuing_order_override: The priority of a task suite among other sets in the pool. Defines the order in which
            task suites are assigned to Tolokers. The larger the parameter value, the higher the priority.
            This parameter can be used if the pool has issue_task_suites_in_creation_order: true.
            Allowed values: from -99999.99999 to 99999.99999.
        mixed: Type of operation for creating a task suite:
            * True - Automatically with the "smart mixing" option (for details, see Toloka requester's guide).
            * False - Manually.
        traits_all_of:
        traits_any_of:
        traits_none_of_any:
        longitude: The longitude of the point on the map for the task suite.
        latitude: The latitude of the point on the map for the task suite.
        id: ID of a task suite. Read only field.
        remaining_overlap: How many times will this Task Suite be issued to Tolokers. Read only field.
        automerged: The task suite flag is created after task merging. Read Only field. Value:
            * True - The task suite is generated as a result of merging identical tasks.
            * False - A standard task suite created by "smart mixing" or by the requester.
        created: The UTC date and time when the task suite was created. Read Only field.
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
    """Parameters for TaskSuite creation controlling

    Attributes:
        operation_id: Operation ID for asynchronous loading of task suites.
        skip_invalid_items: Validation parameters:
            * True - Create the task suites that passed validation. Skip the rest of the task suites.
            * False - If at least one of the task suites didn't pass validation, stop the operation and
                don't create the task suites.
        allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters.
            * False - Use the overlap that is set in the task suite parameters (in the `overlap` field).
        open_pool: Open the pool immediately after creating a task suite, if the pool is closed.
        async_mode: How the request is processed:
            * True — deferred. The query results in an asynchronous operation running in the background.
                Answer contains information about the operation (start and end time, status, number of sets).
            * False — synchronous. Answer contains information about the generated sets of tasks.
                You can send a maximum of 5000 task sets in a single request.
    """

    operation_id: UUID
    skip_invalid_items: bool
    allow_defaults: bool
    open_pool: bool
    async_mode: bool = attribute(default=True)


class TaskSuiteOverlapPatch(BaseTolokaObject):
    """Parameters to stop issuing a specific TaskSuite
    """

    overlap: int


class TaskSuitePatch(InfiniteOverlapParametersMixin, BaseTolokaObject):
    """Parameters for changing specific TaskSuite

    Attributes:
        issuing_order_override: The priority of a task suite among other sets in the pool. Defines the order in which
            task suites are assigned to Tolokers. The larger the parameter value, the higher the priority.
            This parameter can be used if the pool has issue_task_suites_in_creation_order: true.
            Allowed values: from -99999.99999 to 99999.99999.
        open_pool: Open the pool immediately after changing a task suite, if the pool is closed.
    """

    issuing_order_override: float
    open_pool: bool
