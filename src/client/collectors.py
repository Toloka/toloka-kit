"""
https://yandex.ru/dev/toloka/doc/concepts/quality_control-docpage/
"""

from enum import Enum, unique
from typing import ClassVar, FrozenSet, List, Optional
from uuid import UUID

from .conditions import RuleCondition
from .conditions import RuleConditionKey
from .util._codegen import BaseParameters


class CollectorConfig(BaseParameters, spec_enum='Type', spec_field='type'):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]]

    @unique
    class Type(Enum):
        GOLDEN_SET = 'GOLDEN_SET'
        MAJORITY_VOTE = 'MAJORITY_VOTE'
        CAPTCHA = 'CAPTCHA'
        INCOME = 'INCOME'
        SKIPPED_IN_ROW_ASSIGNMENTS = 'SKIPPED_IN_ROW_ASSIGNMENTS'
        ANSWER_COUNT = 'ANSWER_COUNT'
        ASSIGNMENT_SUBMIT_TIME = 'ASSIGNMENT_SUBMIT_TIME'
        ACCEPTANCE_RATE = 'ACCEPTANCE_RATE'
        ASSIGNMENTS_ASSESSMENT = 'ASSIGNMENTS_ASSESSMENT'
        USERS_ASSESSMENT = 'USERS_ASSESSMENT'
        TRAINING = 'TRAINING'

    def validate_condition(self, conditions: List[RuleCondition]):
        incompatible_conditions = [c for c in conditions if c.key not in self._compatible_conditions]
        if incompatible_conditions:
            raise ValueError(f'Incompatible conditions {incompatible_conditions}')

    uuid: UUID


class AcceptanceRate(CollectorConfig, spec_value=CollectorConfig.Type.ACCEPTANCE_RATE):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.TOTAL_ASSIGNMENTS_COUNT,
        RuleConditionKey.ACCEPTED_ASSIGNMENTS_RATE,
        RuleConditionKey.REJECTED_ASSIGNMENTS_RATE,
    ])


class AnswerCount(CollectorConfig, spec_value=CollectorConfig.Type.ANSWER_COUNT):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.ASSIGNMENTS_ACCEPTED_COUNT,
    ])


class AssignmentsAssessment(CollectorConfig, spec_value=CollectorConfig.Type.ASSIGNMENTS_ASSESSMENT):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.PENDING_ASSIGNMENTS_COUNT,
        RuleConditionKey.ACCEPTED_ASSIGNMENTS_COUNT,
        RuleConditionKey.REJECTED_ASSIGNMENTS_COUNT,
        RuleConditionKey.ASSESSMENT_EVENT,
    ])


class AssignmentSubmitTime(CollectorConfig, spec_value=CollectorConfig.Type.ASSIGNMENT_SUBMIT_TIME):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.TOTAL_SUBMITTED_COUNT,
        RuleConditionKey.FAST_SUBMITTED_COUNT,
    ])

    class Parameters(CollectorConfig.Parameters):
        fast_submit_threshold_seconds: int
        history_size: Optional[int] = None


class Captcha(CollectorConfig, spec_value=CollectorConfig.Type.CAPTCHA):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.STORED_RESULTS_COUNT,
        RuleConditionKey.SUCCESS_RATE,
        RuleConditionKey.FAIL_RATE,
    ])

    class Parameters(CollectorConfig.Parameters):
        history_size: Optional[int] = None


class GoldenSet(CollectorConfig, spec_value=CollectorConfig.Type.GOLDEN_SET):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.TOTAL_ANSWERS_COUNT,
        RuleConditionKey.CORRECT_ANSWERS_RATE,
        RuleConditionKey.INCORRECT_ANSWERS_RATE,
        RuleConditionKey.GOLDEN_SET_ANSWERS_COUNT,
        RuleConditionKey.GOLDEN_SET_CORRECT_ANSWERS_RATE,
        RuleConditionKey.GOLDEN_SET_INCORRECT_ANSWERS_RATE,
    ])

    class Parameters(CollectorConfig.Parameters):
        history_size: Optional[int] = None


class Income(CollectorConfig, spec_value=CollectorConfig.Type.INCOME):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.INCOME_SUM_FOR_LAST_24_HOURS,
    ])


class MajorityVote(CollectorConfig, spec_value=CollectorConfig.Type.MAJORITY_VOTE):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.TOTAL_ANSWERS_COUNT,
        RuleConditionKey.CORRECT_ANSWERS_RATE,
        RuleConditionKey.INCORRECT_ANSWERS_RATE,
    ])

    class Parameters(CollectorConfig.Parameters):
        answer_threshold: int
        history_size: Optional[int] = None

    parameters: Parameters


class SkippedInRowAssignments(CollectorConfig, spec_value=CollectorConfig.Type.SKIPPED_IN_ROW_ASSIGNMENTS):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.SKIPPED_IN_ROW_COUNT,
    ])


class Training(CollectorConfig, spec_value=CollectorConfig.Type.TRAINING):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.SUBMITTED_ASSIGNMENTS_COUNT,
        RuleConditionKey.TOTAL_ANSWERS_COUNT,
        RuleConditionKey.CORRECT_ANSWERS_RATE,
        RuleConditionKey.INCORRECT_ANSWERS_RATE,
        RuleConditionKey.NEXT_ASSIGNMENT_AVAILABLE,
    ])


class UsersAssessment(CollectorConfig, spec_value=CollectorConfig.Type.USERS_ASSESSMENT):

    _compatible_conditions: ClassVar[FrozenSet[RuleConditionKey]] = frozenset([
        RuleConditionKey.POOL_ACCESS_REVOKED_REASON,
        RuleConditionKey.SKILL_ID,
    ])
