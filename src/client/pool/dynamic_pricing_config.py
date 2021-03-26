__all__ = ['DynamicPricingConfig']
from enum import Enum, unique
from typing import List

from ..primitives.base import attribute, BaseTolokaObject


class DynamicPricingConfig(BaseTolokaObject, kw_only=False):
    """The dynamic pricing settings.

    Attributes:
        type: Parameter type for calculating dynamic pricing. The SKILL value.
        skill_id: ID of the skill that the task price is based on
        intervals: Skill level intervals. Must not overlap.
            A performer with a skill level that is not included in any interval will receive the basic
            price for a task suite.
    """

    @unique
    class Type(Enum):
        """Dynamic pricing type"""
        SKILL = 'SKILL'

    class Interval(BaseTolokaObject):
        """Skill level interval

        Attributes:
            from_: Lower bound of the interval.
            to: dynamic_pricing_config.intervals.to
            reward_per_assignment: The price per task page for a performer with the specified skill level.
        """

        from_: int = attribute(origin='from')
        to: int
        reward_per_assignment: float

    type: Type
    skill_id: str
    intervals: List[Interval]
