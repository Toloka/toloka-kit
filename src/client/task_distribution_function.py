from enum import Enum, unique
from typing import List

from .primitives.base import attribute, BaseTolokaObject


class TaskDistributionFunction(BaseTolokaObject):

    @unique
    class Scope(Enum):
        PROJECT = 'PROJECT'
        POOL = 'POOL'

    @unique
    class Distribution(Enum):
        UNIFORM = 'UNIFORM'

    class Interval(BaseTolokaObject):
        from_: int = attribute(origin='from')
        to: int
        frequency: int

    scope: Scope
    distribution: Distribution
    window_days: int
    intervals: List[Interval]
