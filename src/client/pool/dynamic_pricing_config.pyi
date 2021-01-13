from enum import Enum
from typing import Any, Dict, List, Optional

from ..primitives.base import BaseTolokaObject


class DynamicPricingConfig(BaseTolokaObject):
    """The dynamic pricing settings.

    Attributes:
        type: Parameter type for calculating dynamic pricing. The SKILL value.
        skill_id: ID of the skill that the task price is based on
        intervals: Skill level intervals. Must not overlap.
            A performer with a skill level that is not included in any interval will receive the basic
            price for a task suite.
    """

    class Type(Enum):
        ...

    class Interval(BaseTolokaObject):
        """Skill level intervals. Must not overlap.

        A performer with a skill level that is not included in any interval will receive the basic
            price for a task suite.
        Attributes:
            from_: Lower bound of the interval.
            to: dynamic_pricing_config.intervals.to
            reward_per_assignment: The price per task page for a performer with the specified skill level.
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
            reward_per_assignment: Optional[float] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        from_: Optional[int]
        to: Optional[int]
        reward_per_assignment: Optional[float]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,
        type: Optional[Type] = ...,
        skill_id: Optional[str] = ...,
        intervals: Optional[List[Interval]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    type: Optional[Type]
    skill_id: Optional[str]
    intervals: Optional[List[Interval]]
