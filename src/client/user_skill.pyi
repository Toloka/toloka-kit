from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class SetUserSkillRequest(BaseTolokaObject):
    """Parameters for setting the skill value of a specific performer

    Used for grouping the fields required for setting the user's skill.
    Usually, when calling TolokaClient.set_user_skill, you can use the expand version, passing all the class attributes to the call.

    Attributes:
        skill_id: Skill ID. What skill to set.
        user_id: User ID. Which user.
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
    """Describes the value of a specific skill for a specific performer

    Attributes:
        id: Internal identifier of the user's skill value.
        skill_id: Skill identifier, which skill is installed.
        user_id: User identifier, to which performer the skill is installed.
        value: Skill value (from 0 to 100). Rough presentation.
        exact_value: Skill value (from 0 to 100). Exact representation.
        created: Date and time when this skill was created for the performer.
        modified: Date and time of the last skill change for the performer.
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
