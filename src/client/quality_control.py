__all__ = ['QualityControl']
from enum import unique
from typing import List

from .actions import RuleAction
from .collectors import CollectorConfig
from .conditions import RuleCondition
from .primitives.base import BaseTolokaObject
from .task_distribution_function import TaskDistributionFunction
from ..util._codegen import attribute
from ..util._extendable_enum import ExtendableStrEnum


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

        training_pool_id: str
        training_passing_skill_value: int

    @unique
    class CaptchaFrequency(ExtendableStrEnum):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

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

            target_overlap: int
            task_distribution_function: TaskDistributionFunction

        real_settings: Settings
        golden_settings: Settings
        training_settings: Settings

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

            action: RuleAction
            conditions: List[RuleCondition]

        rules: List[RuleConfig]
        collector_config: CollectorConfig

    training_requirement: TrainingRequirement
    captcha_frequency: CaptchaFrequency = attribute(autocast=True)
    configs: List[QualityControlConfig] = attribute(factory=list)
    checkpoints_config: CheckpointsConfig

    def add_action(self, collector: CollectorConfig, action: RuleAction, conditions: List[RuleCondition]):
        """Adds new QualityControlConfig to QualityControl object. Usually in pool.

        See example in QualityControl class.

        Arg:
            collector: Parameters for collecting statistics (for example, the number of task skips in the pool).
            action: Action if conditions are met (for example, close access to the project).
            conditions: Conditions (for example, skipping 10 sets of tasks in a row).
        """

        # Checking that conditions are compatible with our collector
        collector.validate_condition(conditions)

        # We can possibly add the action to an existing config
        for config in self.configs:
            if config.collector_config == collector:
                break
        else:
            config = QualityControl.QualityControlConfig(rules=[], collector_config=collector)
            self.configs.append(config)

        rule = QualityControl.QualityControlConfig.RuleConfig(action=action, conditions=conditions)
        config.rules.append(rule)
