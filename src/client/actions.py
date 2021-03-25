__all__ = [
    'RuleType',
    'RuleAction',
    'Restriction',
    'RestrictionV2',
    'SetSkillFromOutputField',
    'ChangeOverlap',
    'SetSkill',
    'RejectAllAssignments',
    'ApproveAllAssignments'
]
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
    """Base class for all actions in quality controls configurations
    """

    pass


class Restriction(RuleAction, spec_value=RuleType.RESTRICTION):
    """Block access to projects or pools

    It's better to use new version: RestrictionV2.

    Attributes:
        parameters.scope:
            * POOL - Current pool where this rule was triggered. Does not affect the user's rating.
            * PROJECT - Current project where this rule was triggered. Affects the user's rating.
            * ALL_PROJECTS - All customer's projects.
        parameters.duration_days: Blocking period in days. By default, the lock is indefinite.
        parameters.private_comment: Comment (reason for blocking). Available only to the customer.
    """

    class Parameters(RuleAction.Parameters):
        scope: UserRestriction.Scope
        duration_days: int
        private_comment: str


class RestrictionV2(RuleAction, spec_value=RuleType.RESTRICTION_V2):
    """Block access to projects or pools

    Attributes:
        parameters.scope:
            * POOL - Current pool where this rule was triggered. Does not affect the user's rating.
            * PROJECT - Current project where this rule was triggered. Affects the user's rating.
            * ALL_PROJECTS - All customer's projects.
        parameters.duration: Blocking period in duration_unit.
        parameters.duration_unit: In what units the restriction duration is measured:
            * MINUTES
            * HOURS
            * DAYS
            * PERMANENT
        parameters.private_comment: Comment (reason for blocking). Available only to the customer.

    Example:
        How to ban performers who answers too fast.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.conditions.FastSubmittedCount > 1],
        >>>     action=toloka.actions.RestrictionV2(
        >>>         scope=toloka.user_restriction.UserRestriction.PROJECT,
        >>>         duration=10,
        >>>         duration_unit='DAYS',
        >>>         private_comment='Fast responses',
        >>>     )
        >>> )
        ...
    """

    class Parameters(RuleAction.Parameters):
        scope: UserRestriction.Scope
        duration: int
        duration_unit: DurationUnit
        private_comment: str


class SetSkillFromOutputField(RuleAction, spec_value=RuleType.SET_SKILL_FROM_OUTPUT_FIELD):
    """Set performer skill value from source

    You can use this rule only with collectors.MajorityVote and collectors.GoldenSet.

    Attributes:
        parameters.skill_id: ID of the skill to update.
        parameters.from_field: The value to assign to the skill:
            * correct_answers_rate - Percentage of correct answers.
            * incorrect_answer_rate - Percentage of incorrect answers.

    Example:
        How to set the skill value to mean consistency with the majority.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.MajorityVote(answer_threshold=2, history_size=10),
        >>>     conditions=[
        >>>         toloka.conditions.TotalAnswersCount > 2,
        >>>     ],
        >>>     action=toloka.actions.SetSkillFromOutputField(
        >>>         skill_id=some_skill_id,
        >>>         from_field='correct_answers_rate',
        >>>     ),
        >>> )
        ...
    """

    class Parameters(RuleAction.Parameters):
        skill_id: str
        from_field: RuleConditionKey


class ChangeOverlap(RuleAction, spec_value=RuleType.CHANGE_OVERLAP):
    """Increase the overlap of the set of tasks (or tasks, if the option is used "smart mixing")

    You can use this rule only with collectors.UsersAssessment and collectors.AssignmentsAssessment.

    Attributes:
        parameters.delta: The number by which you want to increase the overlap of the task set
            (or the task if the option is used "smart mixing").
        parameters.open_pool: Changing the pool status:
            * True - Open the pool after changing if it is closed.
            * False - Do not open the pool after the change if it is closed.

    Example:
        How to increase task overlap when you reject assignment in delayed mode.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentsAssessment(),
        >>>     conditions=[toloka.conditions.AssessmentEvent == toloka.conditions.AssessmentEvent.REJECT],
        >>>     action=toloka.actions.ChangeOverlap(delta=1, open_pool=True),
        >>> )
        ...
    """

    class Parameters(RuleAction.Parameters):
        delta: int
        open_pool: bool


class SetSkill(RuleAction, spec_value=RuleType.SET_SKILL):
    """Set perfmer skill value

    Attributes:
        parameters.skill_id: ID of the skill to update.
        parameters.skill_value: The value to be assigned to the skill.

    Example:
        How to mark performers completing a task so that you can filter them later in the checking project.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AnswerCount(),
        >>>     conditions=[toloka.conditions.AssignmentsAcceptedCount > 0],
        >>>     action=toloka.actions.SetSkill(skill_id=some_skill_id, skill_value=1),
        >>> )
        ...
    """

    class Parameters(RuleAction.Parameters):
        skill_id: str
        skill_value: int


class RejectAllAssignments(RuleAction, spec_value=RuleType.REJECT_ALL_ASSIGNMENTS):
    """Reject all replies from the performer

    The performer is not explicitly installed, the rejection occurs on the performer on which the rule will be triggered.

    Attributes:
        parameters.public_comment: Describes why you reject all assignments from this performer.

    Example:
        How to reject all assignments if performer sends answers too fast.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.conditions.FastSubmittedCount > 3],
        >>>     action=toloka.actions.RejectAllAssignments(public_comment='Too fast answering. You are cheater!')
        >>> )
        ...
    """

    class Parameters(RuleAction.Parameters):
        public_comment: str


class ApproveAllAssignments(RuleAction, spec_value=RuleType.APPROVE_ALL_ASSIGNMENTS):
    """Approve all replies from the performer

    The performer is not explicitly installed, the approval occurs on the performer on which the rule will be triggered.

    Example:
        How to approve all assignments if performer doing well with golden tasks.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.GoldenSet(history_size=5),
        >>>     conditions=[toloka.conditions.GoldenSetCorrectAnswersRate > 90],
        >>>     action=toloka.actions.ApproveAllAssignments()
        >>> )
        ...
    """

    pass
