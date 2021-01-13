from enum import Enum, unique
from typing import List

from ..primitives.base import attribute, BaseTolokaObject


class DynamicPricingConfig(BaseTolokaObject, kw_only=False):

    @unique
    class Type(Enum):
        SKILL = 'SKILL'

    class Interval(BaseTolokaObject):
        from_: int = attribute(origin='from')
        to: int
        reward_per_assignment: float

    type: Type
    skill_id: str
    intervals: List[Interval]
