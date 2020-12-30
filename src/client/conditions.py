from enum import Enum, unique
from typing import Any

from .primitives.base import BaseTolokaObject
from .primitives.operators import IdentityConditionMixin, ComparableConditionMixin


@unique
class RuleConditionKey(Enum):
    ACCEPTED_ASSIGNMENTS_COUNT = 'accepted_assignments_count'
    ACCEPTED_ASSIGNMENTS_RATE = 'accepted_assignments_rate'
    ASSESSMENT_EVENT = 'assessment_event'
    ASSIGNMENTS_ACCEPTED_COUNT = 'assignments_accepted_count'
    CORRECT_ANSWERS_RATE = 'correct_answers_rate'
    FAIL_RATE = 'fail_rate'
    FAST_SUBMITTED_COUNT = 'fast_submitted_count'
    GOLDEN_SET_ANSWERS_COUNT = 'golden_set_answers_count'
    GOLDEN_SET_CORRECT_ANSWERS_RATE = 'golden_set_correct_answers_rate'
    GOLDEN_SET_INCORRECT_ANSWERS_RATE = 'golden_set_incorrect_answers_rate'
    INCOME_SUM_FOR_LAST_24_HOURS = 'income_sum_for_last_24_hours'
    INCORRECT_ANSWERS_RATE = 'incorrect_answers_rate'
    NEXT_ASSIGNMENT_AVAILABLE = 'next_assignment_available'
    PENDING_ASSIGNMENTS_COUNT = 'pending_assignments_count'
    POOL_ACCESS_REVOKED_REASON = 'pool_access_revoked_reason'
    REJECTED_ASSIGNMENTS_COUNT = 'rejected_assignments_count'
    REJECTED_ASSIGNMENTS_RATE = 'rejected_assignments_rate'
    SKILL_ID = 'skill_id'
    SKIPPED_IN_ROW_COUNT = 'skipped_in_row_count'
    STORED_RESULTS_COUNT = 'stored_results_count'
    SUBMITTED_ASSIGNMENTS_COUNT = 'submitted_assignments_count'
    SUCCESS_RATE = 'success_rate'
    TOTAL_ANSWERS_COUNT = 'total_answers_count'
    TOTAL_ASSIGNMENTS_COUNT = 'total_assignments_count'
    TOTAL_SUBMITTED_COUNT = 'total_submitted_count'


class RuleCondition(BaseTolokaObject, spec_enum=RuleConditionKey, spec_field='key'):
    operator: Any
    value: Any


class ComparableRuleCondition(RuleCondition, ComparableConditionMixin):
    pass


class IdentityRuleCondition(RuleCondition, IdentityConditionMixin):
    pass


class AcceptedAssignmentsCount(ComparableRuleCondition, spec_value=RuleConditionKey.ACCEPTED_ASSIGNMENTS_COUNT):
    value: int


class AcceptedAssignmentsRate(ComparableRuleCondition, spec_value=RuleConditionKey.ACCEPTED_ASSIGNMENTS_RATE):
    value: float


class AssessmentEvent(IdentityRuleCondition, spec_value=RuleConditionKey.ASSESSMENT_EVENT):

    @unique
    class Type(Enum):
        ACCEPT = 'ACCEPT'
        REJECT = 'REJECT'

    ACCEPT = Type.ACCEPT
    REJECT = Type.REJECT

    value: Type


class AssignmentsAcceptedCount(ComparableRuleCondition, spec_value=RuleConditionKey.ASSIGNMENTS_ACCEPTED_COUNT):
    value: int


class CorrectAnswersRate(ComparableRuleCondition, spec_value=RuleConditionKey.CORRECT_ANSWERS_RATE):
    value: float


class FailRate(ComparableRuleCondition, spec_value=RuleConditionKey.FAIL_RATE):
    value: float


class FastSubmittedCount(ComparableRuleCondition, spec_value=RuleConditionKey.FAST_SUBMITTED_COUNT):
    value: int


class GoldenSetAnswersCount(ComparableRuleCondition, spec_value=RuleConditionKey.GOLDEN_SET_ANSWERS_COUNT):
    value: int


class GoldenSetCorrectAnswersRate(ComparableRuleCondition, spec_value=RuleConditionKey.GOLDEN_SET_CORRECT_ANSWERS_RATE):
    value: float


class GoldenSetIncorrectAnswersRate(ComparableRuleCondition, spec_value=RuleConditionKey.GOLDEN_SET_INCORRECT_ANSWERS_RATE):
    value: float


class IncomeSumForLast24Hours(ComparableRuleCondition, spec_value=RuleConditionKey.INCOME_SUM_FOR_LAST_24_HOURS):
    value: float


class IncorrectAnswersRate(ComparableRuleCondition, spec_value=RuleConditionKey.INCORRECT_ANSWERS_RATE):
    value: float


class NextAssignmentAvailable(ComparableRuleCondition, spec_value=RuleConditionKey.NEXT_ASSIGNMENT_AVAILABLE):
    value: bool


class PendingAssignmentsCount(ComparableRuleCondition, spec_value=RuleConditionKey.PENDING_ASSIGNMENTS_COUNT):
    value: int


class PoolAccessRevokedReason(IdentityRuleCondition, spec_value=RuleConditionKey.POOL_ACCESS_REVOKED_REASON):

    @unique
    class Type(Enum):
        SKILL_CHANGE = 'SKILL_CHANGE'
        RESTRICTION = 'RESTRICTION'

    SKILL_CHANGE = Type.SKILL_CHANGE
    RESTRICTION = Type.RESTRICTION

    value: Type


class RejectedAssignmentsCount(ComparableRuleCondition, spec_value=RuleConditionKey.REJECTED_ASSIGNMENTS_COUNT):
    value: int


class RejectedAssignmentsRate(ComparableRuleCondition, spec_value=RuleConditionKey.REJECTED_ASSIGNMENTS_RATE):
    value: float


class SkillId(IdentityRuleCondition, spec_value=RuleConditionKey.SKILL_ID):
    value: str


class SkippedInRowCount(ComparableRuleCondition, spec_value=RuleConditionKey.SKIPPED_IN_ROW_COUNT):
    value: int


class StoredResultsCount(ComparableRuleCondition, spec_value=RuleConditionKey.STORED_RESULTS_COUNT):
    value: int


class SubmittedAssignmentsCount(ComparableRuleCondition, spec_value=RuleConditionKey.SUBMITTED_ASSIGNMENTS_COUNT):
    value: int


class SuccessRate(ComparableRuleCondition, spec_value=RuleConditionKey.SUCCESS_RATE):
    value: float


class TotalAnswersCount(ComparableRuleCondition, spec_value=RuleConditionKey.TOTAL_ANSWERS_COUNT):
    value: int


class TotalAssignmentsCount(ComparableRuleCondition, spec_value=RuleConditionKey.TOTAL_ASSIGNMENTS_COUNT):
    value: int


class TotalSubmittedCount(ComparableRuleCondition, spec_value=RuleConditionKey.TOTAL_SUBMITTED_COUNT):
    value: int
