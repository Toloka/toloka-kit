from enum import Enum
from typing import Any, Dict, List, Optional

from .actions import RuleAction
from .collectors import CollectorConfig
from .conditions import RuleCondition
from .primitives.base import BaseTolokaObject
from .task_distribution_function import TaskDistributionFunction


class QualityControl(BaseTolokaObject):
    """Quality control unit settings and pool ID with training tasks

    Quality control lets you get more accurate responses and restrict access to tasks for cheating performers.
    Quality control consists of rules. All rules work independently.

    Attributes:
        training_requirement: Parameters of the training pool that is linked to the pool with the main tasks.
        captcha_frequency: Frequency of captcha display (By default, captcha is not shown):
            LOW - show every 20 tasks.
            MEDIUM, HIGH - show every 10 tasks.
        configs: List of quality control units. See QualityControl.QualityControlConfig
        checkpoints_config: Random check majority opinion. Datailed description in QualityControl.CheckpointsConfig.
    
    Example:
        How to set up quality control on new pool.

        >>> new_pool = toloka.pool.Pool(....)
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.conditions.FastSubmittedCount > 1],
        >>>     action=toloka.actions.RestrictionV2(
        >>>         scope=toloka.user_restriction.UserRestriction.ALL_PROJECTS,
        >>>         duration=10,
        >>>         duration_unit='DAYS',
        >>>         private_comment='Fast responses',  # Only you will see this comment
        >>>     )
        >>> )
        ...
    """

    class TrainingRequirement(BaseTolokaObject):
        """Parameters of the training pool that is linked to the pool with the main tasks

        Attributes:
            training_pool_id: ID of the training pool that is linked to the pool with the main tasks.
            training_passing_skill_value: The percentage of correct answers in training tasks (from 0 to 100) required
                for admission to the main tasks. The user's first responses in tasks are used for counting.
        """

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
            training_pool_id: Optional[str] = ...,
            training_passing_skill_value: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        training_pool_id: Optional[str]
        training_passing_skill_value: Optional[int]

    class CaptchaFrequency(Enum):
        ...

    class CheckpointsConfig(BaseTolokaObject):
        """Random check majority opinion.
        
        Only some tasks are issued with a high overlap (for example, "5") and are being tested.
        Other tasks are issued with the overlap set in the pool settings (for example, "1") and remain without verification.
        Spot check saves money and speeds up pool execution.
        
        You can reduce the frequency of checks over time.

        Example settings: in the first 25 tasks completed by the user in the pool, issue every fifth task with an overlap "5"
        to check the answers. In subsequent tasks issue each 25 task with an overlap "5".

        Attributes:
            real_settings: Checkpoints settings for main tasks.
            golden_settings: Checkpoints settings for golden tasks.
            training_settings: Checkpoints settings for train tasks.
        """

        class Settings(BaseTolokaObject):
            """Setting for checkpoints

            Attributes:
                target_overlap: Overlap in tasks with majority opinion verification.
                task_distribution_function: Distribution of tasks with majority opinion verification.
            """

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
                target_overlap: Optional[int] = ...,
                task_distribution_function: Optional[TaskDistributionFunction] = ...
            ) -> None: ...

            _unexpected: Optional[Dict[str, Any]]
            target_overlap: Optional[int]
            task_distribution_function: Optional[TaskDistributionFunction]

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
            real_settings: Optional[Settings] = ...,
            golden_settings: Optional[Settings] = ...,
            training_settings: Optional[Settings] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        real_settings: Optional[Settings]
        golden_settings: Optional[Settings]
        training_settings: Optional[Settings]

    class QualityControlConfig(BaseTolokaObject):
        """Quality control block

        Quality control blocks help regulate access to a project or pool: you can filter out users who give incorrect answers
        in control tasks, skip many tasks in a row, and so on.

        The block consists of two parts: condition and the action to be performed when the condition is met.
        There may be several conditions, then they are combined using logical And.

        Attributes:
            rules: Conditions and action if conditions are met.
            collector_config: Parameters for collecting statistics (for example, the number of task skips in the pool).
        """

        class RuleConfig(BaseTolokaObject):
            """Conditions and action if conditions are met

            The values for the conditions are taken from the collector.

            Attributes:
                action: Action if conditions are met (for example, close access to the project).
                conditions: Conditions (for example, skipping 10 sets of tasks in a row).
            """

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
                action: Optional[RuleAction] = ...,
                conditions: Optional[List[RuleCondition]] = ...
            ) -> None: ...

            _unexpected: Optional[Dict[str, Any]]
            action: Optional[RuleAction]
            conditions: Optional[List[RuleCondition]]

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
            rules: Optional[List[RuleConfig]] = ...,
            collector_config: Optional[CollectorConfig] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        rules: Optional[List[RuleConfig]]
        collector_config: Optional[CollectorConfig]

    def add_action(
        self,
        collector: CollectorConfig,
        action: RuleAction,
        conditions: List[RuleCondition]
    ): 
        """Adds new QualityControlConfig to QualityControl object. Usually in pool.

        See example in QualityControl class.

        Arg:
            collector: Parameters for collecting statistics (for example, the number of task skips in the pool).
            action: Action if conditions are met (for example, close access to the project).
            conditions: Conditions (for example, skipping 10 sets of tasks in a row).
        """
        ...

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
        training_requirement: Optional[TrainingRequirement] = ...,
        captcha_frequency: Optional[CaptchaFrequency] = ...,
        configs: Optional[List[QualityControlConfig]] = ...,
        checkpoints_config: Optional[CheckpointsConfig] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    training_requirement: Optional[TrainingRequirement]
    captcha_frequency: Optional[CaptchaFrequency]
    configs: Optional[List[QualityControlConfig]]
    checkpoints_config: Optional[CheckpointsConfig]
