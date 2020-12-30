import datetime

from .primitives.base import BaseTolokaObject


class SetUserSkillRequest(BaseTolokaObject):
    skill_id: str
    user_id: str
    value: float


class UserSkill(BaseTolokaObject):
    id: str
    skill_id: str
    user_id: str
    value: int
    exact_value: float
    created: datetime.datetime
    modified: datetime.datetime
