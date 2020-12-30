import datetime
from typing import Dict

from .primitives.base import BaseTolokaObject

LangIso639 = str


class Skill(BaseTolokaObject):
    name: str

    private_comment: str
    hidden: bool
    skill_ttl_hours: int
    training: bool

    public_name: Dict[LangIso639, str]
    public_requester_description: Dict[LangIso639, str]

    # Readonly
    id: str
    created: datetime.datetime
