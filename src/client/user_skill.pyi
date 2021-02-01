from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class SetUserSkillRequest(BaseTolokaObject):
    """SetUserSkillRequest

    Attributes:
        skill_id: Skill ID.
        user_id: User ID.
        value: Fractional value of the skill. Minimum - 0, maximum - 100.
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
        skill_id: Optional[str] = ...,
        user_id: Optional[str] = ...,
        value: Optional[Decimal] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    skill_id: Optional[str]
    user_id: Optional[str]
    value: Optional[Decimal]

class UserSkill(BaseTolokaObject):

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
        skill_id: Optional[str] = ...,
        user_id: Optional[str] = ...,
        value: Optional[int] = ...,
        exact_value: Optional[Decimal] = ...,
        created: Optional[datetime] = ...,
        modified: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    skill_id: Optional[str]
    user_id: Optional[str]
    value: Optional[int]
    exact_value: Optional[Decimal]
    created: Optional[datetime]
    modified: Optional[datetime]
