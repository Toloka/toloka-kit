from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject
from .primitives.parameter import Parameters
from .solution import Solution
from .task import Task


class Assignment(BaseTolokaObject):
    """Contains information about an assigned task suite and the results

    Attributes:
        id: ID of the task suite assignment to a user.
        task_suite_id: ID of a task suite.
        pool_id: ID of the pool that the task suite belongs to.
        user_id: ID of the user who was assigned the task suite.
        status: Status of an assigned task suite.
        reward: Payment received by the performer.
        tasks: Data for the tasks.
        automerged: Flag of the response received as a result of merging identical tasks. Value:
            * True — The response was recorded when identical tasks were merged.
            * False — Normal user response.
        created: The date and time when the task suite was assigned to a user.
        submitted: The date and time when the task suite was completed by a user.
        accepted: The date and time when the responses for the task suite were accepted by the requester.
        rejected: The date and time when the responses for the task suite were rejected by the requester.
        skipped: The date and time when the task suite was skipped by the user.
        expired: The date and time when the time for completing the task suite expired.
        first_declined_solution_attempt: For training tasks. The user's first responses in the training task
            (only if these were the wrong answers). If the user answered correctly on the first try, the
            first_declined_solution_attempt array is omitted.
            Arrays with the responses (output_values) are arranged in the same order as the task data in the tasks array.
        solutions: User responses. Arranged in the same order as the data for tasks in the tasks array.
        mixed: Type of operation for creating a task suite:
            * True — Automatic ("smart mixing").
            * False — Manually.
        public_comment: Optional[str]
    """

    class Status(Enum):
        """Status of an assigned task suite:

        * ACTIVE — Being completed by a user.
        * SUBMITTED — Completed but not checked.
        * ACCEPTED — Accepted by the requester.
        * REJECTED — Rejected by the requester.
        * SKIPPED — Skipped by the user.
        * EXPIRED — The time for completing the tasks expired.
        """
        ...

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
        task_suite_id: Optional[str] = ...,
        pool_id: Optional[str] = ...,
        user_id: Optional[str] = ...,
        status: Optional[Status] = ...,
        reward: Optional[Decimal] = ...,
        tasks: Optional[List[Task]] = ...,
        automerged: Optional[bool] = ...,
        created: Optional[datetime] = ...,
        submitted: Optional[datetime] = ...,
        accepted: Optional[datetime] = ...,
        rejected: Optional[datetime] = ...,
        skipped: Optional[datetime] = ...,
        expired: Optional[datetime] = ...,
        first_declined_solution_attempt: Optional[List[Solution]] = ...,
        solutions: Optional[List[Solution]] = ...,
        mixed: Optional[bool] = ...,
        public_comment: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    task_suite_id: Optional[str]
    pool_id: Optional[str]
    user_id: Optional[str]
    status: Optional[Status]
    reward: Optional[Decimal]
    tasks: Optional[List[Task]]
    automerged: Optional[bool]
    created: Optional[datetime]
    submitted: Optional[datetime]
    accepted: Optional[datetime]
    rejected: Optional[datetime]
    skipped: Optional[datetime]
    expired: Optional[datetime]
    first_declined_solution_attempt: Optional[List[Solution]]
    solutions: Optional[List[Solution]]
    mixed: Optional[bool]
    public_comment: Optional[str]

class AssignmentPatch(BaseTolokaObject):

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
        public_comment: Optional[str] = ...,
        status: Optional[Assignment.Status] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    public_comment: Optional[str]
    status: Optional[Assignment.Status]

class GetAssignmentsTsvParameters(Parameters):

    class Status(Enum):
        ...

    class Field(Enum):
        ...

    def unstructure(self) -> dict: ...

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
        status: Optional[List[Status]] = ...,
        start_time_from: Optional[datetime] = ...,
        start_time_to: Optional[datetime] = ...,
        exclude_banned: Optional[bool] = ...,
        field: Optional[List[Field]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status: Optional[List[Status]]
    start_time_from: Optional[datetime]
    start_time_to: Optional[datetime]
    exclude_banned: Optional[bool]
    field: Optional[List[Field]]
