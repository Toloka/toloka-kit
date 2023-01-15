__all__ = ['MixerConfig']

from ..primitives.base import BaseTolokaObject
from ..task_distribution_function import TaskDistributionFunction
from ...util._codegen import attribute


class MixerConfig(BaseTolokaObject):
    """Settings for automatically grouping tasks into suites (smart mixing).

    You can set the number of general, training and control tasks in a task suite. Also, you control task shuffling and other settings.

    Attributes:
        real_tasks_count: The number of general tasks in a task suite.

            If `training_task_distribution_function` or `golden_task_distribution_function` are used then `real_tasks_count` denotes the maximum number of tasks in a task suite.
        golden_tasks_count: The number of control tasks in a task suite.
        training_tasks_count: The number of training tasks in a task suite.
        min_real_tasks_count: The minimum number of general tasks in a task suite if there are not enough tasks left to create a full task suite.

            Allowed range: from 0 to `real_tasks_count`.
            By default, the `min_real_tasks_count` value equals to the `real_tasks_count` value.
        min_golden_tasks_count: The minimum number of control tasks in a task suite if there are not enough control tasks left to create a full task suite.

            Allowed range: from 0 to `golden_tasks_count`.
            By default, the `min_golden_tasks_count` value equals to the `golden_tasks_count` value.
        min_training_tasks_count: The minimum number of training tasks in a task suite if there are not enough training tasks left to create a full task suite.

            Allowed range: from 0 to `training_tasks_count`.
            By default, the `min_training_tasks_count` value equals to the `training_tasks_count` value.
        force_last_assignment: A setting used when the number of remaining general tasks in the pool is less than the `min_real_tasks_count` value.
            Note, that there must be enough control and training tasks to create a task suite.

            * True — An incomplete task suite is assigned.
            * False — An incomplete task suite is not assigned. It is useful if you add tasks to an open pool.

            Default: `True`.
        force_last_assignment_delay_seconds: Time in seconds before assigning the last task suite. This parameter is used if `force_last_assignment` is set to `True`.

            Allowed range: from 0 to 86,400 seconds (one day).
        mix_tasks_in_creation_order:
            * True — Tasks are grouped in task suites in the order they were created.
            * False — Tasks are chosen for a task suite in a random order.
        shuffle_tasks_in_task_suite:
            * True — Tasks in a task suite are shuffled on the page.
            * False — Tasks in a task suite are placed on the page in the order they were created.
        golden_task_distribution_function: Customizing the number of control tasks in a task suite depending on completed tasks by a Toloker.
        training_task_distribution_function: Customizing the number of training tasks in a task suite depending on completed tasks by a Toloker.
    """

    real_tasks_count: int = attribute(default=0, required=True)
    golden_tasks_count: int = attribute(default=0, required=True)
    training_tasks_count: int = attribute(default=0, required=True)
    min_real_tasks_count: int
    min_golden_tasks_count: int
    min_training_tasks_count: int
    force_last_assignment: bool
    force_last_assignment_delay_seconds: int
    mix_tasks_in_creation_order: bool
    shuffle_tasks_in_task_suite: bool
    golden_task_distribution_function: TaskDistributionFunction
    training_task_distribution_function: TaskDistributionFunction
