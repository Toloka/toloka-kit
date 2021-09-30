__all__ = [
    'dynamic_overlap_config',
    'dynamic_pricing_config',
    'mixer_config',
    'Pool',
    'PoolPatchRequest',
    'DynamicOverlapConfig',
    'DynamicPricingConfig',
    'MixerConfig',
]
import datetime
import toloka.client.filter
import toloka.client.owner
import toloka.client.pool.dynamic_overlap_config
import toloka.client.pool.dynamic_pricing_config
import toloka.client.pool.mixer_config
import toloka.client.primitives.base
import toloka.client.quality_control
import toloka.client.task_distribution_function
import toloka.util._extendable_enum
import typing

from toloka.client.pool import (
    dynamic_overlap_config,
    dynamic_pricing_config,
    mixer_config
)
from toloka.client.pool.dynamic_overlap_config import DynamicOverlapConfig
from toloka.client.pool.dynamic_pricing_config import DynamicPricingConfig
from toloka.client.pool.mixer_config import MixerConfig

class Pool(toloka.client.primitives.base.BaseTolokaObject):
    """A set of tasks that are issued and checked according to the same rules within the project

    Groups tasks by the following criteria: one-time start-up, which performers can perform tasks, quality control,
    price for TaskSuite's, overlap.
    Tasks, golden tasks and assignments are related to a pool.

    Attributes:
        project_id: ID of the project that the pool was created for.
        private_name: Name of the pool (only visible to the requester).
        may_contain_adult_content: Whether the tasks contain adult content.
        reward_per_assignment: Payment per task suite in U.S. dollars. For cents, use the dot (".") as the separator.
            The minimum payment is $0.01.
            Only training and control tasks can be uploaded to zero-price pools.
        assignment_max_duration_seconds: The time allowed for completing a task suite, in seconds.
            Tasks not completed within this time are reassigned to other users.
            We recommend allowing no more than 60 seconds per task suite (including the time for page loading
            and sending responses).
        defaults: Settings that are applied by default when uploading new task suites to a pool.
        will_expire: The date and time in UTC when the pool should be closed (even if all the task suites haven't
            been completed).
        private_comment: Comments on the pool (only visible to the requester).
        public_description: Description for users. If it is filled in, the text will be displayed instead of
            the project's public_description in the list of tasks for performers.
        public_instructions: Optional[str]
        auto_close_after_complete_delay_seconds: Waiting time (in seconds) before automatic closure of the pool
            after all tasks are completed. Minimum — 0, maximum — 259200 seconds (three days).
            Use it if:
                * Your data processing is close to real time.
                * You need an open pool where you upload tasks.
                * Dynamic overlap is enabled in the pool (dynamic_overlap_config).
        dynamic_pricing_config: The dynamic pricing settings.
        auto_accept_solutions: Whether tasks must be checked manually:
            * True - Automatic task acceptance (manual checking isn't necessary).
            * False - The requester will check the tasks.
        auto_accept_period_day: Optional[int]
        assignments_issuing_config: Settings for assigning tasks in the pool.
        priority: The priority of the pool in relation to other pools in the project with the same task
            price and set of filters. Users are assigned tasks with a higher priority first.
            Possible values: from -100 to 100.
            If the project has multiple pools, the order for completing them depends on the parameters:
            * Pools with identical filter settings and price per task are assigned to users in the order
                in which they were started. The pool that was started earlier will be completed sooner.
                You can change the order for completing the pools.
            * Pools with different filter settings and/or a different price per task are sent out for completion
                when the pool opens.
        filter: Settings for user selection filters.
        quality_control: Settings for quality control rules and the ID of the pool with training tasks.
        dynamic_overlap_config: Dynamic overlap setting. Allows you to change the overlap depending on
            how well the performers handle the task.
        mixer_config: Parameters for automatically creating a task suite (“smart mixing”).
        training_config: Optional[TrainingConfig]
        metadata: Optional[Dict[str, List[str]]]
        owner: Optional[Owner]
        id: Pool ID. Read only field.
        status: Status of the pool. Read only field.
        last_close_reason: The reason for closing the pool the last time. Read only field.
        created: When this pool was created. Read only field.
        last_started: The date and time when the pool was last started. Read only field.
        last_stopped: The date and time when the pool was last stopped. Read only field.
        type: Types of pool. Read only field.

    Example:
        How to create a new pool in a project.

        >>> toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
        >>> new_pool = toloka.pool.Pool(
        >>>     project_id=existing_project_id,
        >>>     private_name='Pool 1',
        >>>     may_contain_adult_content=False,
        >>>     will_expire=datetime.datetime.utcnow() + datetime.timedelta(days=365),
        >>>     reward_per_assignment=0.01,
        >>>     assignment_max_duration_seconds=60*20,
        >>>     defaults=toloka.pool.Pool.Defaults(default_overlap_for_new_task_suites=3),
        >>>     filter=toloka.filter.Languages.in_('EN'),
        >>> )
        >>> new_pool.set_mixer_config(real_tasks_count=10)
        >>> new_pool.quality_control.add_action(...)
        >>> new_pool = toloka_client.create_pool(new_pool)
        >>> print(new_pool.id)
        ...
    """

    class AssignmentsIssuingConfig(toloka.client.primitives.base.BaseTolokaObject):
        """Settings for assigning tasks in the pool.

        Attributes:
            issue_task_suites_in_creation_order: For pools that don't use “smart mixing”.
                Assign task suites in the order in which they were uploaded. For example, for a pool with an
                overlap of 5, the first task suite is assigned to five users, then the second task suite, and so on.
                This parameter is available when the project has "assignments_issuing_type": "AUTOMATED".
        """

        def __init__(self, issue_task_suites_in_creation_order: typing.Optional[bool] = None) -> None:
            """Method generated by attrs for class Pool.AssignmentsIssuingConfig.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        issue_task_suites_in_creation_order: typing.Optional[bool]

    class CloseReason(toloka.util._extendable_enum.ExtendableStrEnum):
        """The reason for closing the pool the last time:

        Attributes:
            MANUAL: Closed by the requester.
            EXPIRED: Reached the date and time set in will_expire.
            COMPLETED: Closed automatically because all the pool tasks were completed.
            NOT_ENOUGH_BALANCE: Closed automatically because the Toloka account ran out of funds.
            ASSIGNMENTS_LIMIT_EXCEEDED: Closed automatically because it exceeded the limit on assigned task suites
                (maximum of 2 million).
            BLOCKED: Closed automatically because the requester's account was blocked by a Toloka administrator.
        """

        MANUAL = 'MANUAL'
        EXPIRED = 'EXPIRED'
        COMPLETED = 'COMPLETED'
        NOT_ENOUGH_BALANCE = 'NOT_ENOUGH_BALANCE'
        ASSIGNMENTS_LIMIT_EXCEEDED = 'ASSIGNMENTS_LIMIT_EXCEEDED'
        BLOCKED = 'BLOCKED'
        FOR_UPDATE = 'FOR_UPDATE'

    class Defaults(toloka.client.primitives.base.BaseTolokaObject):
        """Settings that are applied by default when uploading new task suites to a pool.

        Attributes:
            default_overlap_for_new_task_suites: The overlap for task suites that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
            default_overlap_for_new_tasks: The overlap for tasks that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
        """

        def __init__(
            self,
            *,
            default_overlap_for_new_task_suites: typing.Optional[int] = None,
            default_overlap_for_new_tasks: typing.Optional[int] = None
        ) -> None:
            """Method generated by attrs for class Pool.Defaults.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        default_overlap_for_new_task_suites: typing.Optional[int]
        default_overlap_for_new_tasks: typing.Optional[int]

    class Status(toloka.util._extendable_enum.ExtendableStrEnum):
        """Status of the pool

        Attributes:
            OPEN: Pool is open
            CLOSED: Pool is closed
            ARCHIVED: Pool is archived
            LOCKED: Pool is locked
        """

        OPEN = 'OPEN'
        CLOSED = 'CLOSED'
        ARCHIVED = 'ARCHIVED'
        LOCKED = 'LOCKED'

    class TrainingConfig(toloka.client.primitives.base.BaseTolokaObject):
        def __init__(self, training_skill_ttl_days: typing.Optional[int] = None) -> None:
            """Method generated by attrs for class Pool.TrainingConfig.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        training_skill_ttl_days: typing.Optional[int]

    class Type(toloka.util._extendable_enum.ExtendableStrEnum):
        """An enumeration.
        """

        REGULAR = 'REGULAR'
        TRAINING = 'TRAINING'

    def unstructure(self) -> typing.Optional[dict]: ...

    def is_open(self) -> bool: ...

    def is_closed(self) -> bool: ...

    def is_archived(self) -> bool: ...

    def is_locked(self) -> bool: ...

    @typing.overload
    def set_training_requirement(self, training_requirement: toloka.client.quality_control.QualityControl.TrainingRequirement):
        """A shortcut setter for quality_control.training_requirement
        """
        ...

    @typing.overload
    def set_training_requirement(
        self,
        *,
        training_pool_id: typing.Optional[str] = None,
        training_passing_skill_value: typing.Optional[int] = None
    ):
        """A shortcut setter for quality_control.training_requirement
        """
        ...

    @typing.overload
    def set_captcha_frequency(self, captcha_frequency: toloka.client.quality_control.QualityControl.CaptchaFrequency):
        """A shortcut setter for quality_control.captcha_frequency
        """
        ...

    @typing.overload
    def set_captcha_frequency(
        self,
        *args,
        **kwargs
    ):
        """A shortcut setter for quality_control.captcha_frequency
        """
        ...

    @typing.overload
    def set_checkpoints_config(self, checkpoints_config: toloka.client.quality_control.QualityControl.CheckpointsConfig):
        """A shortcut setter for quality_control.checkpoints_config
        """
        ...

    @typing.overload
    def set_checkpoints_config(
        self,
        *,
        real_settings: typing.Optional[toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings] = None,
        golden_settings: typing.Optional[toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings] = None,
        training_settings: typing.Optional[toloka.client.quality_control.QualityControl.CheckpointsConfig.Settings] = None
    ):
        """A shortcut setter for quality_control.checkpoints_config
        """
        ...

    def set_quality_control_configs(self, configs):
        """A shortcut method for setting
        """
        ...

    def __init__(
        self,
        *,
        project_id: typing.Optional[str] = None,
        private_name: typing.Optional[str] = None,
        may_contain_adult_content: typing.Optional[bool] = None,
        reward_per_assignment: typing.Optional[float] = None,
        assignment_max_duration_seconds: typing.Optional[int] = None,
        defaults: typing.Optional[Defaults] = ...,
        will_expire: typing.Optional[datetime.datetime] = None,
        private_comment: typing.Optional[str] = None,
        public_description: typing.Optional[str] = None,
        public_instructions: typing.Optional[str] = None,
        auto_close_after_complete_delay_seconds: typing.Optional[int] = None,
        dynamic_pricing_config: typing.Optional[toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig] = None,
        auto_accept_solutions: typing.Optional[bool] = None,
        auto_accept_period_day: typing.Optional[int] = None,
        assignments_issuing_config: typing.Optional[AssignmentsIssuingConfig] = None,
        priority: typing.Optional[int] = None,
        filter: typing.Optional[toloka.client.filter.FilterCondition] = None,
        quality_control: typing.Optional[toloka.client.quality_control.QualityControl] = ...,
        dynamic_overlap_config: typing.Optional[toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig] = None,
        mixer_config: typing.Optional[toloka.client.pool.mixer_config.MixerConfig] = None,
        training_config: typing.Optional[TrainingConfig] = None,
        metadata: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
        owner: typing.Optional[toloka.client.owner.Owner] = None,
        id: typing.Optional[str] = None,
        status: typing.Optional[Status] = None,
        last_close_reason: typing.Optional[CloseReason] = None,
        created: typing.Optional[datetime.datetime] = None,
        last_started: typing.Optional[datetime.datetime] = None,
        last_stopped: typing.Optional[datetime.datetime] = None,
        type: typing.Optional[Type] = None
    ) -> None:
        """Method generated by attrs for class Pool.
        """
        ...

    @typing.overload
    def set_defaults(self, defaults: Defaults):
        """A shortcut setter for defaults
        """
        ...

    @typing.overload
    def set_defaults(
        self,
        *,
        default_overlap_for_new_task_suites: typing.Optional[int] = None,
        default_overlap_for_new_tasks: typing.Optional[int] = None
    ):
        """A shortcut setter for defaults
        """
        ...

    @typing.overload
    def set_dynamic_pricing_config(self, dynamic_pricing_config: toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig):
        """A shortcut setter for dynamic_pricing_config
        """
        ...

    @typing.overload
    def set_dynamic_pricing_config(
        self,
        type: typing.Union[toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig.Type, str, None] = None,
        skill_id: typing.Optional[str] = None,
        intervals: typing.Optional[typing.List[toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig.Interval]] = None
    ):
        """A shortcut setter for dynamic_pricing_config
        """
        ...

    @typing.overload
    def set_assignments_issuing_config(self, assignments_issuing_config: AssignmentsIssuingConfig):
        """A shortcut setter for assignments_issuing_config
        """
        ...

    @typing.overload
    def set_assignments_issuing_config(self, issue_task_suites_in_creation_order: typing.Optional[bool] = None):
        """A shortcut setter for assignments_issuing_config
        """
        ...

    @typing.overload
    def set_filter(self, filter: toloka.client.filter.FilterCondition):
        """A shortcut setter for filter
        """
        ...

    @typing.overload
    def set_filter(self):
        """A shortcut setter for filter
        """
        ...

    @typing.overload
    def set_quality_control(self, quality_control: toloka.client.quality_control.QualityControl):
        """A shortcut setter for quality_control
        """
        ...

    @typing.overload
    def set_quality_control(
        self,
        *,
        training_requirement: typing.Optional[toloka.client.quality_control.QualityControl.TrainingRequirement] = None,
        captcha_frequency: typing.Union[toloka.client.quality_control.QualityControl.CaptchaFrequency, str, None] = None,
        configs: typing.Optional[typing.List[toloka.client.quality_control.QualityControl.QualityControlConfig]] = ...,
        checkpoints_config: typing.Optional[toloka.client.quality_control.QualityControl.CheckpointsConfig] = None
    ):
        """A shortcut setter for quality_control
        """
        ...

    @typing.overload
    def set_dynamic_overlap_config(self, dynamic_overlap_config: toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig):
        """A shortcut setter for dynamic_overlap_config
        """
        ...

    @typing.overload
    def set_dynamic_overlap_config(
        self,
        *,
        type: typing.Union[toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Type, str, None] = None,
        max_overlap: typing.Optional[int] = None,
        min_confidence: typing.Optional[float] = None,
        answer_weight_skill_id: typing.Optional[str] = None,
        fields: typing.Optional[typing.List[toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Field]] = None
    ):
        """A shortcut setter for dynamic_overlap_config
        """
        ...

    @typing.overload
    def set_mixer_config(self, mixer_config: toloka.client.pool.mixer_config.MixerConfig):
        """A shortcut setter for mixer_config
        """
        ...

    @typing.overload
    def set_mixer_config(
        self,
        *,
        real_tasks_count: int = 0,
        golden_tasks_count: int = 0,
        training_tasks_count: int = 0,
        min_real_tasks_count: typing.Optional[int] = None,
        min_golden_tasks_count: typing.Optional[int] = None,
        min_training_tasks_count: typing.Optional[int] = None,
        force_last_assignment: typing.Optional[bool] = None,
        force_last_assignment_delay_seconds: typing.Optional[int] = None,
        mix_tasks_in_creation_order: typing.Optional[bool] = None,
        shuffle_tasks_in_task_suite: typing.Optional[bool] = None,
        golden_task_distribution_function: typing.Optional[toloka.client.task_distribution_function.TaskDistributionFunction] = None,
        training_task_distribution_function: typing.Optional[toloka.client.task_distribution_function.TaskDistributionFunction] = None
    ):
        """A shortcut setter for mixer_config
        """
        ...

    @typing.overload
    def set_training_config(self, training_config: TrainingConfig):
        """A shortcut setter for training_config
        """
        ...

    @typing.overload
    def set_training_config(self, training_skill_ttl_days: typing.Optional[int] = None):
        """A shortcut setter for training_config
        """
        ...

    @typing.overload
    def set_owner(self, owner: toloka.client.owner.Owner):
        """A shortcut setter for owner
        """
        ...

    @typing.overload
    def set_owner(
        self,
        *,
        id: typing.Optional[str] = None,
        myself: typing.Optional[bool] = None,
        company_id: typing.Optional[str] = None
    ):
        """A shortcut setter for owner
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    project_id: typing.Optional[str]
    private_name: typing.Optional[str]
    may_contain_adult_content: typing.Optional[bool]
    reward_per_assignment: typing.Optional[float]
    assignment_max_duration_seconds: typing.Optional[int]
    defaults: typing.Optional[Defaults]
    will_expire: typing.Optional[datetime.datetime]
    private_comment: typing.Optional[str]
    public_description: typing.Optional[str]
    public_instructions: typing.Optional[str]
    auto_close_after_complete_delay_seconds: typing.Optional[int]
    dynamic_pricing_config: typing.Optional[toloka.client.pool.dynamic_pricing_config.DynamicPricingConfig]
    auto_accept_solutions: typing.Optional[bool]
    auto_accept_period_day: typing.Optional[int]
    assignments_issuing_config: typing.Optional[AssignmentsIssuingConfig]
    priority: typing.Optional[int]
    filter: typing.Optional[toloka.client.filter.FilterCondition]
    quality_control: typing.Optional[toloka.client.quality_control.QualityControl]
    dynamic_overlap_config: typing.Optional[toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig]
    mixer_config: typing.Optional[toloka.client.pool.mixer_config.MixerConfig]
    training_config: typing.Optional[TrainingConfig]
    metadata: typing.Optional[typing.Dict[str, typing.List[str]]]
    owner: typing.Optional[toloka.client.owner.Owner]
    id: typing.Optional[str]
    status: typing.Optional[Status]
    last_close_reason: typing.Optional[CloseReason]
    created: typing.Optional[datetime.datetime]
    last_started: typing.Optional[datetime.datetime]
    last_stopped: typing.Optional[datetime.datetime]
    type: typing.Optional[Type]


class PoolPatchRequest(toloka.client.primitives.base.BaseTolokaObject):
    """Class for changing the priority of the pool issue

    To do this use TolokaClient.patch_pool(). You can use expanded version, then pass "priority" directly to "patch_pool".

    Attributes:
        priority: The priority of the pool in relation to other pools in the project with the same task
            price and set of filters. Users are assigned tasks with a higher priority first.
            Possible values: from -100 to 100.

    Example:
        How to set highest priority to some pool.

        >>> toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
        >>> patched_pool = toloka_client.patch_pool(existing_pool_id, 100)
        >>> print(patched_pool.priority)
        ...
    """

    def __init__(self, priority: typing.Optional[int] = None) -> None:
        """Method generated by attrs for class PoolPatchRequest.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    priority: typing.Optional[int]
