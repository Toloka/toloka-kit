__all__ = [
    'QualityControl',
]
import toloka.client.actions
import toloka.client.collectors
import toloka.client.conditions
import toloka.client.primitives.base
import toloka.client.task_distribution_function
import toloka.util._extendable_enum
import typing


class QualityControl(toloka.client.primitives.base.BaseTolokaObject):
    """Quality control settings.

    Quality control lets you get more accurate responses, restrict access to tasks for Tolokers who give responses of low quality, and filter out robots.

    Attributes:
        configs: A list of quality control rules configurations.
        checkpoints_config: A selective majority vote check configuration.
        training_requirement: Parameters for linking a training pool to a general task pool.
        captcha_frequency: **Deprecated.** A frequency of showing captchas.
            * `LOW` — Show one for every 20 tasks.
            * `MEDIUM`, `HIGH` — Show one for every 10 tasks.

            By default, captchas aren't displayed.

    Example:
        A quality control rule that restricts access if a Toloker responds too fast.

        >>> new_pool = toloka.client.pool.Pool()
        >>> new_pool.quality_control.add_action(
        >>>     collector=toloka.client.collectors.AssignmentSubmitTime(history_size=5, fast_submit_threshold_seconds=20),
        >>>     conditions=[toloka.client.conditions.FastSubmittedCount > 1],
        >>>     action=toloka.client.actions.RestrictionV2(
        >>>         scope=toloka.client.user_restriction.UserRestriction.ALL_PROJECTS,
        >>>         duration=10,
        >>>         duration_unit='DAYS',
        >>>         private_comment='Fast responses',
        >>>     )
        >>> )
        ...
    """

    class TrainingRequirement(toloka.client.primitives.base.BaseTolokaObject):
        """Parameters for linking a training pool to a general task pool.

        Attributes:
            training_pool_id: The ID of the training pool.
            training_passing_skill_value: The percentage of correct answers in training tasks required in order to access the general tasks.
                Only the first answer of the Toloker in each task is taken into account.

                Allowed values: from 0 to 100.
        """

        def __init__(
            self,
            *,
            training_pool_id: typing.Optional[str] = None,
            training_passing_skill_value: typing.Optional[int] = None
        ) -> None:
            """Method generated by attrs for class QualityControl.TrainingRequirement.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        training_pool_id: typing.Optional[str]
        training_passing_skill_value: typing.Optional[int]

    class CaptchaFrequency(toloka.util._extendable_enum.ExtendableStrEnum):
        """An enumeration.
        """

        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    class CheckpointsConfig(toloka.client.primitives.base.BaseTolokaObject):
        """A selective majority vote check configuration.

        This quality control method checks some of Toloker's responses against the majority of Tolokers. To do this, it changes the overlap of those tasks.

        An example of the configuration:
            * For the first 100 tasks completed by a Toloker in the pool, every 5th task is checked. The overlap of these tasks is increased to 5.
            * After completing 100 tasks, every 25th task is checked.

        Learn more about the [Selective majority vote check](https://toloka.ai/docs/guide/selective-mvote/).

        Attributes:
            real_settings: Selective majority vote settings for general tasks.
            golden_settings: Selective majority vote settings for control tasks.
            training_settings: Selective majority vote settings for training tasks.
        """

        class Settings(toloka.client.primitives.base.BaseTolokaObject):
            """Selective majority vote check settings.

            Attributes:
                target_overlap: The overlap value used for selected tasks that are checked.
                task_distribution_function: The configuration of selecting tasks.
            """

            def __init__(
                self,
                *,
                target_overlap: typing.Optional[int] = None,
                task_distribution_function: typing.Optional[toloka.client.task_distribution_function.TaskDistributionFunction] = None
            ) -> None:
                """Method generated by attrs for class QualityControl.CheckpointsConfig.Settings.
                """
                ...

            _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
            target_overlap: typing.Optional[int]
            task_distribution_function: typing.Optional[toloka.client.task_distribution_function.TaskDistributionFunction]

        def __init__(
            self,
            *,
            real_settings: typing.Optional[Settings] = None,
            golden_settings: typing.Optional[Settings] = None,
            training_settings: typing.Optional[Settings] = None
        ) -> None:
            """Method generated by attrs for class QualityControl.CheckpointsConfig.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        real_settings: typing.Optional[Settings]
        golden_settings: typing.Optional[Settings]
        training_settings: typing.Optional[Settings]

    class QualityControlConfig(toloka.client.primitives.base.BaseTolokaObject):
        """A quality control rules configuration.

        A rule consists of conditions, and an action to perform when the conditions are met. The rule conditions use statistics provided by a connected collector.

        An example of the configuration.
        Toloka collects statistics of skipped tasks. If 10 task suites are skipped in a row, then a Toloker can no longer access a project.

        To learn more, see:
        * [Quality control rules](https://toloka.ai/docs/api/quality_control/) in the API.
        * [Quality control rules](https://toloka.ai/docs/guide/control/) in the guide.

        Attributes:
            rules: The conditions and the action.
            collector_config: The configuration of the collector.
        """

        class RuleConfig(toloka.client.primitives.base.BaseTolokaObject):
            """Rule conditions and an action.

            The action is performed if conditions are met. Multiple conditions are combined with the AND operator.

            Attributes:
                action: The action.
                conditions: A list of conditions.
            """

            def __init__(
                self,
                *,
                action: typing.Optional[toloka.client.actions.RuleAction] = None,
                conditions: typing.Optional[typing.List[toloka.client.conditions.RuleCondition]] = None
            ) -> None:
                """Method generated by attrs for class QualityControl.QualityControlConfig.RuleConfig.
                """
                ...

            _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
            action: typing.Optional[toloka.client.actions.RuleAction]
            conditions: typing.Optional[typing.List[toloka.client.conditions.RuleCondition]]

        def __init__(
            self,
            *,
            rules: typing.Optional[typing.List[RuleConfig]] = None,
            collector_config: typing.Optional[toloka.client.collectors.CollectorConfig] = None
        ) -> None:
            """Method generated by attrs for class QualityControl.QualityControlConfig.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        rules: typing.Optional[typing.List[RuleConfig]]
        collector_config: typing.Optional[toloka.client.collectors.CollectorConfig]

    def add_action(
        self,
        collector: toloka.client.collectors.CollectorConfig,
        action: toloka.client.actions.RuleAction,
        conditions: typing.List[toloka.client.conditions.RuleCondition]
    ):
        """Adds a quality control rule configuration.

        See an example in the description of the [QualityControl](toloka.client.quality_control.QualityControl.md) class.

        Args:
            collector: A collector that provides statistics.
            conditions: Conditions based on statistics.
            action: An action performed if all conditions are met.
        """
        ...

    def __init__(
        self,
        *,
        training_requirement: typing.Optional[TrainingRequirement] = None,
        captcha_frequency: typing.Union[CaptchaFrequency, str, None] = None,
        configs: typing.Optional[typing.List[QualityControlConfig]] = ...,
        checkpoints_config: typing.Optional[CheckpointsConfig] = None
    ) -> None:
        """Method generated by attrs for class QualityControl.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    training_requirement: typing.Optional[TrainingRequirement]
    captcha_frequency: typing.Optional[CaptchaFrequency]
    configs: typing.Optional[typing.List[QualityControlConfig]]
    checkpoints_config: typing.Optional[CheckpointsConfig]
