__all__ = ['TaskDistributionFunction']
from enum import unique
from typing import List

from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._extendable_enum import ExtendableStrEnum


class TaskDistributionFunction(BaseTolokaObject):
    """Issue of tasks with uneven frequency

    Can be used for:
    - Distribution of tasks with majority opinion verification.
    - Issuing control tasks with uneven frequency. Allows you to change the frequency of verification as the user completes tasks.
    - Issuing training tasks with uneven frequency. Allows you to change the frequency of training tasks as the user completes tasks.

    Attributes:
        scope: How to count tasks completed by the user:
            * POOL - Count completed pool tasks.
            * PROJECT - Count completed project tasks.
        distribution: Distribution of tasks within an interval. Parameter has only one possible:
            value - UNIFORM.
        window_days: Period in which completed tasks are counted (number of days).
        intervals: Interval borders and number of tasks in an interval.
    """

    @unique
    class Scope(ExtendableStrEnum):
        PROJECT = 'PROJECT'
        POOL = 'POOL'

    @unique
    class Distribution(ExtendableStrEnum):
        UNIFORM = 'UNIFORM'

    class Interval(BaseTolokaObject):
        """Interval borders and number of tasks in an interval

        Attributes:
            from_: Start of the interval (number of task completed by the user in the project or in the pool).
            to: End of the interval (number of task completed by the user in the project or in the pool).
            frequency: Frequency of tasks in an interval. The first task in an interval is a distributed task.
                For example, if you set frequency: 3 tasks number 1, 4, 7 and so on will be distributed tasks.
        """

        from_: int = attribute(origin='from')
        to: int
        frequency: int

    scope: Scope = attribute(autocast=True)
    distribution: Distribution = attribute(autocast=True)
    window_days: int
    intervals: List[Interval]
