__all__ = [
    'SetUserSkillRequest',
    'UserSkill'
]
from attr.validators import optional, instance_of
import datetime
from decimal import Decimal

from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute


class SetUserSkillRequest(BaseTolokaObject):
    """Parameters for setting the skill value of a specific Toloker.

    These parameters are used by the [set_user_skill](toloka.client.TolokaClient.set_user_skill.md) method.

    Attributes:
        skill_id: The ID of the skill to set.
        user_id: Toloker's ID.
        value: The value of the skill. Allowed values: from 0 to 100.
    """

    skill_id: str
    user_id: str
    value: Decimal = attribute(validator=optional(instance_of(Decimal)))


class UserSkill(BaseTolokaObject):
    """A Toloker's skill value.

    Attributes:
        id: The ID of the Toloker's skill value.
        skill_id: The skill ID.
        user_id: The Toloker ID.
        exact_value: The fractional value of the skill. Allowed values: from 0 to 100.
        value: The integer value of the skill. It is the `exact_value` rounded to the nearest integer.
        created: The date and time when the skill was assigned the first time.
        modified: The date and time when the skill value was updated.
    """

    id: str
    skill_id: str
    user_id: str
    value: int
    exact_value: Decimal = attribute(validator=optional(instance_of(Decimal)))
    created: datetime.datetime
    modified: datetime.datetime
