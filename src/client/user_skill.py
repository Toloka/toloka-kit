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

    Used for grouping the fields required for setting the Toloker's skill.
    Usually, when calling TolokaClient.set_user_skill, you can use the expand version, passing all the class attributes to the call.

    Attributes:
        skill_id: Skill ID. What skill to set.
        user_id: Toloker's ID.
        value: Fractional value of the skill. Minimum - 0, maximum - 100.
    """

    skill_id: str
    user_id: str
    value: Decimal = attribute(validator=optional(instance_of(Decimal)))


class UserSkill(BaseTolokaObject):
    """Describes the value of a specific skill for a specific Toloker.

    Attributes:
        id: Internal identifier of the Toloker's skill value.
        skill_id: Skill identifier, which skill is installed.
        user_id: Toloker identifier, to which Toloker the skill is installed.
        value: Skill value (from 0 to 100). Rough presentation.
        exact_value: Skill value (from 0 to 100). Exact representation.
        created: Date and time when this skill was created for the Toloker.
        modified: Date and time of the last skill change for the Toloker.
    """

    id: str
    skill_id: str
    user_id: str
    value: int
    exact_value: Decimal = attribute(validator=optional(instance_of(Decimal)))
    created: datetime.datetime
    modified: datetime.datetime
