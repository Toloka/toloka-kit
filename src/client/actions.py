from enum import Enum, unique

from .conditions import RuleConditionKey
from .user_restriction import DurationUnit, UserRestriction
from .util._codegen import BaseParameters


@unique
class RuleType(Enum):
    RESTRICTION = 'RESTRICTION'
    RESTRICTION_V2 = 'RESTRICTION_V2'
    SET_SKILL_FROM_OUTPUT_FIELD = 'SET_SKILL_FROM_OUTPUT_FIELD'
    CHANGE_OVERLAP = 'CHANGE_OVERLAP'
    SET_SKILL = 'SET_SKILL'
    REJECT_ALL_ASSIGNMENTS = 'REJECT_ALL_ASSIGNMENTS'
    APPROVE_ALL_ASSIGNMENTS = 'APPROVE_ALL_ASSIGNMENTS'


class RuleAction(BaseParameters, spec_enum=RuleType, spec_field='type'):
    pass


class Restriction(RuleAction, spec_value=RuleType.RESTRICTION):

    class Parameters(RuleAction.Parameters):
        scope: UserRestriction.Scope
        duration_days: int
        private_comment: str


class RestrictionV2(RuleAction, spec_value=RuleType.RESTRICTION_V2):

    class Parameters(RuleAction.Parameters):
        scope: UserRestriction.Scope
        duration: int
        duration_unit: DurationUnit
        private_comment: str


class SetSkillFromOutputField(RuleAction, spec_value=RuleType.SET_SKILL_FROM_OUTPUT_FIELD):

    class Parameters(RuleAction.Parameters):
        skill_id: str
        from_field: RuleConditionKey


class ChangeOverlap(RuleAction, spec_value=RuleType.CHANGE_OVERLAP):

    class Parameters(RuleAction.Parameters):
        delta: int
        open_pool: bool


class SetSkill(RuleAction, spec_value=RuleType.SET_SKILL):

    class Parameters(RuleAction.Parameters):
        skill_id: str
        skill_value: int


class RejectAllAssignments(RuleAction, spec_value=RuleType.REJECT_ALL_ASSIGNMENTS):

    class Parameters(RuleAction.Parameters):
        public_comment: str


class ApproveAllAssignments(RuleAction, spec_value=RuleType.APPROVE_ALL_ASSIGNMENTS):
    pass
