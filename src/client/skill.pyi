from datetime import datetime
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class Skill(BaseTolokaObject):
    """Skill

    A skill is an assessment of some aspect of a user's responses (a number from 0 to 100).
    You can set up skill calculation in a quality control rule, or manually set the skill level for a user.
    You can use skills to select users who perform pool tasks.
    Attributes:
        name: Skill name.
        private_comment: Comments on the skill (only visible to the requester).
        hidden: Access to information about the skill (the name and value) for users:
            * True — closed
            * False — open
        skill_ttl_hours: The skill's "time to live" after the last update (in hours). The skill is removed from
            the user's profile if the skill level hasn't been updated for the specified length of time.
        training: Whether the skill is related to a training pool:
            * True — The skill level is calculated from training pool tasks.
            * False — The skill isn't related to a training pool.
        public_name: Optional[Dict[str, str]]
        public_requester_description: Optional[Dict[str, str]]
        id: Skill ID.
        created: The UTC date and time when the skill was created.
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
        name: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        hidden: Optional[bool] = ...,
        skill_ttl_hours: Optional[int] = ...,
        training: Optional[bool] = ...,
        public_name: Optional[Dict[str, str]] = ...,
        public_requester_description: Optional[Dict[str, str]] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    name: Optional[str]
    private_comment: Optional[str]
    hidden: Optional[bool]
    skill_ttl_hours: Optional[int]
    training: Optional[bool]
    public_name: Optional[Dict[str, str]]
    public_requester_description: Optional[Dict[str, str]]
    id: Optional[str]
    created: Optional[datetime]
