from enum import Enum
from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject


class TaskDistributionFunction(BaseTolokaObject):
    """Issue of training tasks with uneven frequency.

    Attributes:
        scope: How to count tasks completed by the user:
            * POOL — Count completed pool tasks.
            * PROJECT — Count completed project tasks.
        distribution: Distribution of training tasks within an interval. Parameter has only one possible
            value — UNIFORM.
        window_days: Period in which completed tasks are counted (number of days).
        intervals: Interval borders and number of control tasks in an interval.
    """

    class Scope(Enum):
        ...

    class Distribution(Enum):
        ...

    class Interval(BaseTolokaObject):
        """Interval borders and number of control tasks in an interval.

        Attributes:
            from_: Start of the interval (number of task completed by the user in the project or in the pool).
            to: End of the interval (number of task completed by the user in the project or in the pool).
            frequency: Frequency of training tasks in an interval. The first task in an interval is a training task.
                For example, if you set frequency: 3 tasks number 1, 4, 7 and so on will be training tasks.
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
            from_: Optional[int] = ...,
            to: Optional[int] = ...,
            frequency: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        from_: Optional[int]
        to: Optional[int]
        frequency: Optional[int]

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
        scope: Optional[Scope] = ...,
        distribution: Optional[Distribution] = ...,
        window_days: Optional[int] = ...,
        intervals: Optional[List[Interval]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    scope: Optional[Scope]
    distribution: Optional[Distribution]
    window_days: Optional[int]
    intervals: Optional[List[Interval]]
