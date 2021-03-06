from datetime import datetime
from typing import Any, Dict, List, Optional, overload
from uuid import UUID

from .primitives.base import BaseTolokaObject
from .primitives.infinite_overlap import InfiniteOverlapParametersMixin
from .primitives.parameter import Parameters
from .task import BaseTask


class TaskSuite(InfiniteOverlapParametersMixin, BaseTolokaObject):
    """A task suite is a set of tasks placed on the same webpage. 

    Attributes:
        pool_id: The ID of the pool that tasks are uploaded to.
        tasks: Data for the tasks.
        reserved_for: IDs of users who will have access to the task suite.
        unavailable_for: IDs of users who shouldn't have access to the task suite.
        issuing_order_override: The priority of a task suite among other sets in the pool. Defines the order in which
            task suites are assigned to performers. The larger the parameter value, the higher the priority.
            This parameter can be used if the pool has issue_task_suites_in_creation_order: true.
            Allowed values: from -99999.99999 to 99999.99999.
        mixed: Type of operation for creating a task suite:
            * True — Automatically with the “smart mixing” option (for details, see Yandex.Toloka requester's guide).
            * False — Manually.
        traits_all_of: Optional[List[str]]
        traits_any_of: Optional[List[str]]
        traits_none_of_any: Optional[List[str]]
        longitude: The longitude of the point on the map for the task suite.
        latitude: The latitude of the point on the map for the task suite.
        id: ID of a task suite.
        remaining_overlap: Optional[int]
        automerged: The task suite flag is created after task merging. Value:
            * True — The task suite is generated as a result of merging identical tasks.
            * False — A standard task suite created by “smart mixing” or by the requester.
        created: The UTC date and time when the task suite was created.
    """

    @overload
    def add_base_task(
        self,*,
        input_values: Optional[Dict[str, Any]] = ...,
        known_solutions: Optional[List[BaseTask.KnownSolution]] = ...,
        message_on_unknown_solution: Optional[str] = ...,
        id: Optional[str] = ...,
        origin_task_id: Optional[str] = ...
    ) -> 'TaskSuite': ...

    @overload
    def add_base_task(self, base_task: BaseTask) -> 'TaskSuite': ...

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
        infinite_overlap=...,
        overlap=...,
        pool_id: Optional[str] = ...,
        tasks: Optional[List[BaseTask]] = ...,
        reserved_for: Optional[List[str]] = ...,
        unavailable_for: Optional[List[str]] = ...,
        issuing_order_override: Optional[float] = ...,
        mixed: Optional[bool] = ...,
        traits_all_of: Optional[List[str]] = ...,
        traits_any_of: Optional[List[str]] = ...,
        traits_none_of_any: Optional[List[str]] = ...,
        longitude: Optional[float] = ...,
        latitude: Optional[float] = ...,
        id: Optional[str] = ...,
        remaining_overlap: Optional[int] = ...,
        automerged: Optional[bool] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    pool_id: Optional[str]
    tasks: Optional[List[BaseTask]]
    reserved_for: Optional[List[str]]
    unavailable_for: Optional[List[str]]
    issuing_order_override: Optional[float]
    mixed: Optional[bool]
    traits_all_of: Optional[List[str]]
    traits_any_of: Optional[List[str]]
    traits_none_of_any: Optional[List[str]]
    longitude: Optional[float]
    latitude: Optional[float]
    id: Optional[str]
    remaining_overlap: Optional[int]
    automerged: Optional[bool]
    created: Optional[datetime]

class TaskSuiteCreateRequestParameters(Parameters):
    """TaskSuiteCreateRequestParameters

    Attributes:
        operation_id: Operation ID for asynchronous loading of task suites
        skip_invalid_items: Validation parameters:
            * True — Create the task suites that passed validation. Skip the rest of the task suites.
            * False — If at least one of the task suites didn't pass validation, stop the operation and
                don't create the task suites.
        allow_defaults: Overlap settings:
            * True - Use the overlap that is set in the pool parameters.
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
        operation_id: Optional[UUID] = ...,
        skip_invalid_items: Optional[bool] = ...,
        allow_defaults: Optional[bool] = ...,
        open_pool: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operation_id: Optional[UUID]
    skip_invalid_items: Optional[bool]
    allow_defaults: Optional[bool]
    open_pool: Optional[bool]

class TaskSuiteOverlapPatch(BaseTolokaObject):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, overlap: Optional[int] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    overlap: Optional[int]

class TaskSuitePatch(InfiniteOverlapParametersMixin, BaseTolokaObject):

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
        infinite_overlap=...,
        overlap=...,
        issuing_order_override: Optional[float] = ...,
        open_pool: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    issuing_order_override: Optional[float]
    open_pool: Optional[bool]
