from enum import Enum
from typing import Any, Dict, Optional, overload

from .conditions import RuleConditionKey
from .user_restriction import DurationUnit, UserRestriction
from .util._codegen import BaseParameters


class RuleType(Enum):
    ...

class RuleAction(BaseParameters):
    """Base class for all actions in quality controls configurations
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(
        self,*,
        parameters: Optional[BaseParameters.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[BaseParameters.Parameters]

class Restriction(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

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
            scope: Optional[UserRestriction.Scope] = ...,
            duration_days: Optional[int] = ...,
            private_comment: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        scope: Optional[UserRestriction.Scope]
        duration_days: Optional[int]
        private_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        scope: Optional[UserRestriction.Scope] = ...,
        duration_days: Optional[int] = ...,
        private_comment: Optional[str] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class RestrictionV2(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

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
            scope: Optional[UserRestriction.Scope] = ...,
            duration: Optional[int] = ...,
            duration_unit: Optional[DurationUnit] = ...,
            private_comment: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        scope: Optional[UserRestriction.Scope]
        duration: Optional[int]
        duration_unit: Optional[DurationUnit]
        private_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        scope: Optional[UserRestriction.Scope] = ...,
        duration: Optional[int] = ...,
        duration_unit: Optional[DurationUnit] = ...,
        private_comment: Optional[str] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class SetSkillFromOutputField(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

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
            skill_id: Optional[str] = ...,
            from_field: Optional[RuleConditionKey] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skill_id: Optional[str]
        from_field: Optional[RuleConditionKey]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        skill_id: Optional[str] = ...,
        from_field: Optional[RuleConditionKey] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class ChangeOverlap(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

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
            delta: Optional[int] = ...,
            open_pool: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        delta: Optional[int]
        open_pool: Optional[bool]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        delta: Optional[int] = ...,
        open_pool: Optional[bool] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class SetSkill(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

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
            skill_id: Optional[str] = ...,
            skill_value: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skill_id: Optional[str]
        skill_value: Optional[int]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        skill_id: Optional[str] = ...,
        skill_value: Optional[int] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class RejectAllAssignments(RuleAction):
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

    class Parameters(BaseParameters.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, public_comment: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        public_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self, *, public_comment: Optional[str] = ...) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class ApproveAllAssignments(RuleAction):
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

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(
        self,*,
        parameters: Optional[BaseParameters.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[BaseParameters.Parameters]
