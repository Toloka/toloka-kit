from attr.validators import optional, instance_of
import datetime
from decimal import Decimal

from .primitives.base import attribute, BaseTolokaObject


class SetUserSkillRequest(BaseTolokaObject):
    skill_id: str
    user_id: str
    value: Decimal = attribute(validator=optional(instance_of(Decimal)))


class UserSkill(BaseTolokaObject):
    id: str
    skill_id: str
    user_id: str
    value: int
    exact_value: Decimal = attribute(validator=optional(instance_of(Decimal)))
    created: datetime.datetime
    modified: datetime.datetime
