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
from enum import unique
from typing import Dict, List, Optional

import attr

from . import dynamic_overlap_config
from . import dynamic_pricing_config
from . import mixer_config

from .dynamic_overlap_config import DynamicOverlapConfig
from .dynamic_pricing_config import DynamicPricingConfig
from .mixer_config import MixerConfig
from .._converter import unstructure
from ..filter import FilterCondition, FilterOr, FilterAnd
from ..owner import Owner
from ..primitives.base import BaseTolokaObject
from ..quality_control import QualityControl
from ...util._codegen import attribute, codegen_attr_attributes_setters, create_setter, expand
from ...util._extendable_enum import ExtendableStrEnum


@codegen_attr_attributes_setters
class Pool(BaseTolokaObject):
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

    class AssignmentsIssuingConfig(BaseTolokaObject, kw_only=False):
        """Settings for assigning tasks in the pool.

        Attributes:
            issue_task_suites_in_creation_order: For pools that don't use “smart mixing”.
                Assign task suites in the order in which they were uploaded. For example, for a pool with an
                overlap of 5, the first task suite is assigned to five users, then the second task suite, and so on.
                This parameter is available when the project has "assignments_issuing_type": "AUTOMATED".
        """

        issue_task_suites_in_creation_order: bool

    @unique
    class CloseReason(ExtendableStrEnum):
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

    class Defaults(BaseTolokaObject):
        """Settings that are applied by default when uploading new task suites to a pool.

        Attributes:
            default_overlap_for_new_task_suites: The overlap for task suites that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
            default_overlap_for_new_tasks: The overlap for tasks that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
        """

        default_overlap_for_new_task_suites: int
        default_overlap_for_new_tasks: int

    @unique
    class Status(ExtendableStrEnum):
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

    class TrainingConfig(BaseTolokaObject, kw_only=False):
        training_skill_ttl_days: int

    @unique
    class Type(ExtendableStrEnum):
        REGULAR = 'REGULAR'
        TRAINING = 'TRAINING'

    DynamicOverlapConfig = DynamicOverlapConfig
    DynamicPricingConfig = DynamicPricingConfig
    MixerConfig = MixerConfig
    QualityControl = QualityControl

    project_id: str
    private_name: str
    may_contain_adult_content: bool
    reward_per_assignment: float
    assignment_max_duration_seconds: int
    defaults: Defaults = attr.attrib(factory=lambda: Pool.Defaults(default_overlap_for_new_task_suites=1))

    will_expire: datetime.datetime

    private_comment: str
    public_description: str
    public_instructions: str
    auto_close_after_complete_delay_seconds: int
    dynamic_pricing_config: DynamicPricingConfig

    auto_accept_solutions: bool
    auto_accept_period_day: int
    assignments_issuing_config: AssignmentsIssuingConfig
    priority: int
    filter: FilterCondition
    quality_control: QualityControl = attr.attrib(factory=QualityControl)
    dynamic_overlap_config: DynamicOverlapConfig
    mixer_config: MixerConfig
    training_config: TrainingConfig

    metadata: Dict[str, List[str]]
    owner: Owner

    # Readonly
    id: str = attribute(readonly=True)
    status: Status = attribute(readonly=True)
    last_close_reason: CloseReason = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)
    last_started: datetime.datetime = attribute(readonly=True)
    last_stopped: datetime.datetime = attribute(readonly=True)
    type: Type = attribute(readonly=True)

    def unstructure(self) -> Optional[dict]:
        self_unstructured_dict = super().unstructure()
        if self.filter is not None and not isinstance(self.filter, (FilterOr, FilterAnd)):
            self_unstructured_dict['filter'] = unstructure(FilterAnd([self.filter]))
        return self_unstructured_dict

    def is_open(self) -> bool:
        return self.status == Pool.Status.OPEN

    def is_closed(self) -> bool:
        return self.status == Pool.Status.CLOSED

    def is_archived(self) -> bool:
        return self.status == Pool.Status.ARCHIVED

    def is_locked(self) -> bool:
        return self.status == Pool.Status.LOCKED

    set_training_requirement = expand('training_requirement')(create_setter(
        'quality_control.training_requirement',
        QualityControl.TrainingRequirement,
        __name__,
    ))

    set_captcha_frequency = expand('captcha_frequency')(create_setter(
        'quality_control.captcha_frequency',
        QualityControl.CaptchaFrequency,
        __name__,
    ))

    set_checkpoints_config = expand('checkpoints_config')(create_setter(
        'quality_control.checkpoints_config',
        QualityControl.CheckpointsConfig,
        __name__,
    ))

    set_quality_control_configs = create_setter('quality_control.configs', module=__name__)
    set_quality_control_configs.__doc__ = """A shortcut method for setting """


class PoolPatchRequest(BaseTolokaObject, kw_only=False):
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

    priority: int
