from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from ..filter import FilterCondition
from ..owner import Owner
from .dynamic_overlap_config import DynamicOverlapConfig
from .dynamic_pricing_config import DynamicPricingConfig
from .mixer_config import MixerConfig
from ..primitives.base import BaseTolokaObject
from ..quality_control import QualityControl


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
        id: Pool ID.  Read only field.
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
        >>> new_pool.set_mixer_config(real_tasks_count=10, golden_tasks_count=0, training_tasks_count=0)
        >>> new_pool.quality_control.add_action(...)
        >>> new_pool = toloka_client.create_pool(new_pool)
        >>> print(new_pool.id)
        ...
    """

    class AssignmentsIssuingConfig(BaseTolokaObject):
        """Settings for assigning tasks in the pool.

        Attributes:
            issue_task_suites_in_creation_order: For pools that don't use “smart mixing”.
                Assign task suites in the order in which they were uploaded. For example, for a pool with an
                overlap of 5, the first task suite is assigned to five users, then the second task suite, and so on.
                This parameter is available when the project has "assignments_issuing_type": "AUTOMATED".
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
            self,
            issue_task_suites_in_creation_order: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        issue_task_suites_in_creation_order: Optional[bool]

    class CloseReason(Enum):
        """The reason for closing the pool the last time:

        * MANUAL — Closed by the requester.
        * EXPIRED — Reached the date and time set in will_expire.
        * COMPLETED — Closed automatically because all the pool tasks were completed.
        * NOT_ENOUGH_BALANCE — Closed automatically because the Toloka account ran out of funds.
        * ASSIGNMENTS_LIMIT_EXCEEDED — Closed automatically because it exceeded the limit on assigned task suites
            (maximum of 2 million).
        * BLOCKED — Closed automatically because the requester's account was blocked by a Toloka administrator.
        """
        ...

    class Defaults(BaseTolokaObject):
        """Settings that are applied by default when uploading new task suites to a pool.

        Attributes:
            default_overlap_for_new_task_suites: The overlap for task suites that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
            default_overlap_for_new_tasks: The overlap for tasks that are uploaded to the pool
                (used if the allow_defaults=True parameter is set when uploading).
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
            default_overlap_for_new_task_suites: Optional[int] = ...,
            default_overlap_for_new_tasks: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        default_overlap_for_new_task_suites: Optional[int]
        default_overlap_for_new_tasks: Optional[int]

    class Status(Enum):
        """Status of the pool:

        * OPEN
        * CLOSED
        * ARCHIVED
        """
        ...

    class TrainingConfig(BaseTolokaObject):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, training_skill_ttl_days: Optional[int] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        training_skill_ttl_days: Optional[int]

    class Type(Enum):
        ...

    def unstructure(self) -> Optional[dict]: ...

    def is_open(self) -> bool: ...

    def is_closed(self) -> bool: ...

    def is_archived(self) -> bool: ...

    def is_locked(self) -> bool: ...

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
        project_id: Optional[str] = ...,
        private_name: Optional[str] = ...,
        may_contain_adult_content: Optional[bool] = ...,
        reward_per_assignment: Optional[float] = ...,
        assignment_max_duration_seconds: Optional[int] = ...,
        defaults: Optional[Defaults] = ...,
        will_expire: Optional[datetime] = ...,
        private_comment: Optional[str] = ...,
        public_description: Optional[str] = ...,
        public_instructions: Optional[str] = ...,
        auto_close_after_complete_delay_seconds: Optional[int] = ...,
        dynamic_pricing_config: Optional[DynamicPricingConfig] = ...,
        auto_accept_solutions: Optional[bool] = ...,
        auto_accept_period_day: Optional[int] = ...,
        assignments_issuing_config: Optional[AssignmentsIssuingConfig] = ...,
        priority: Optional[int] = ...,
        filter: Optional[FilterCondition] = ...,
        quality_control: Optional[QualityControl] = ...,
        dynamic_overlap_config: Optional[DynamicOverlapConfig] = ...,
        mixer_config: Optional[MixerConfig] = ...,
        training_config: Optional[TrainingConfig] = ...,
        metadata: Optional[Dict[str, List[str]]] = ...,
        owner: Optional[Owner] = ...,
        id: Optional[str] = ...,
        status: Optional[Status] = ...,
        last_close_reason: Optional[CloseReason] = ...,
        created: Optional[datetime] = ...,
        last_started: Optional[datetime] = ...,
        last_stopped: Optional[datetime] = ...,
        type: Optional[Type] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    project_id: Optional[str]
    private_name: Optional[str]
    may_contain_adult_content: Optional[bool]
    reward_per_assignment: Optional[float]
    assignment_max_duration_seconds: Optional[int]
    defaults: Optional[Defaults]
    will_expire: Optional[datetime]
    private_comment: Optional[str]
    public_description: Optional[str]
    public_instructions: Optional[str]
    auto_close_after_complete_delay_seconds: Optional[int]
    dynamic_pricing_config: Optional[DynamicPricingConfig]
    auto_accept_solutions: Optional[bool]
    auto_accept_period_day: Optional[int]
    assignments_issuing_config: Optional[AssignmentsIssuingConfig]
    priority: Optional[int]
    filter: Optional[FilterCondition]
    quality_control: Optional[QualityControl]
    dynamic_overlap_config: Optional[DynamicOverlapConfig]
    mixer_config: Optional[MixerConfig]
    training_config: Optional[TrainingConfig]
    metadata: Optional[Dict[str, List[str]]]
    owner: Optional[Owner]
    id: Optional[str]
    status: Optional[Status]
    last_close_reason: Optional[CloseReason]
    created: Optional[datetime]
    last_started: Optional[datetime]
    last_stopped: Optional[datetime]
    type: Optional[Type]

class PoolPatchRequest(BaseTolokaObject):
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

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, priority: Optional[int] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    priority: Optional[int]
