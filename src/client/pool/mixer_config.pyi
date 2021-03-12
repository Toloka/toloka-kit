from typing import Any, Dict, Optional

from ..primitives.base import BaseTolokaObject
from ..task_distribution_function import TaskDistributionFunction


class MixerConfig(BaseTolokaObject):
    """Parameters for automatically creating a task suite ("smart mixing").

    For more information about creating task see Yandex.Toloka Requester's guide.
    Attributes:
        real_tasks_count: The number of main tasks to put in a task suite.
            The maximum number of tasks in a task suite if training_task_distribution_function or
            golden_task_distribution_function are used.
        golden_tasks_count: The number of control ("golden set") tasks to put in a task suite.
        training_tasks_count: The number of training tasks to put in a task suite.
        min_real_tasks_count: Minimum number of main tasks in a task suite (if the number of assignments left is less
            than the one specified in real_tasks_count). Minimum — 0. By default, the value is the same as in
            real_tasks_count.
        min_golden_tasks_count: Minimum number of control tasks in a task suite (if the number of assignments left is
            less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same as
            in golden_tasks_count.
        min_training_tasks_count: Minimum number of training tasks in a task suite (if the number of assignments left is
            less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same
            as in training_tasks_count.
        force_last_assignment: Setup for the last set of tasks in the pool, if less than the minimum remaining number of
            tasks are not completed (mixer_config.min_real_tasks_count). Values:
            * true - issue an incomplete task set.
            * false - don't issue tasks. This option can be used if you are adding tasks after the pool is started.
            This parameter only applies to main tasks. The number of control and training tasks in the last set must be
            complete (golden_tasks_count, training_tasks_count).
        force_last_assignment_delay_seconds: Waiting time (in seconds) since the addition of the task, or increase in
            the overlap, prior to the issuance of the last set of tasks in the pool. The minimum is 0, the maximum is
            86,400 seconds (one day).
            This parameter can be used if the pool has force_last_assignment: True.
        mix_tasks_in_creation_order: The order for including tasks in suites:
            * True — Add tasks to suites in the order in which they were uploaded. For example, in a pool with an
                overlap of 5, the first uploaded task will be included in the first 5 task suites. They will be
                assigned to 5 users.
            * False — Add tasks to suites in random order.
        shuffle_tasks_in_task_suite: The order of tasks within a suite:
            * True — Random.
            * False — The order in which tasks were uploaded.
        golden_task_distribution_function: Issue of control tasks with uneven frequency. The option allows you to change
            the frequency of checking as the user completes more tasks.
        training_task_distribution_function: Issue of training tasks with uneven frequency. The option allows you to
            change the frequency of training tasks as the user completes more tasks.
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
        real_tasks_count: Optional[int] = ...,
        golden_tasks_count: Optional[int] = ...,
        training_tasks_count: Optional[int] = ...,
        min_real_tasks_count: Optional[int] = ...,
        min_golden_tasks_count: Optional[int] = ...,
        min_training_tasks_count: Optional[int] = ...,
        force_last_assignment: Optional[bool] = ...,
        force_last_assignment_delay_seconds: Optional[int] = ...,
        mix_tasks_in_creation_order: Optional[bool] = ...,
        shuffle_tasks_in_task_suite: Optional[bool] = ...,
        golden_task_distribution_function: Optional[TaskDistributionFunction] = ...,
        training_task_distribution_function: Optional[TaskDistributionFunction] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    real_tasks_count: Optional[int]
    golden_tasks_count: Optional[int]
    training_tasks_count: Optional[int]
    min_real_tasks_count: Optional[int]
    min_golden_tasks_count: Optional[int]
    min_training_tasks_count: Optional[int]
    force_last_assignment: Optional[bool]
    force_last_assignment_delay_seconds: Optional[int]
    mix_tasks_in_creation_order: Optional[bool]
    shuffle_tasks_in_task_suite: Optional[bool]
    golden_task_distribution_function: Optional[TaskDistributionFunction]
    training_task_distribution_function: Optional[TaskDistributionFunction]
