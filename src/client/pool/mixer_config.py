from ..primitives.base import BaseTolokaObject
from ..task_distribution_function import TaskDistributionFunction


class MixerConfig(BaseTolokaObject):
    real_tasks_count: int
    golden_tasks_count: int
    training_tasks_count: int
    min_real_tasks_count: int
    min_golden_tasks_count: int
    min_training_tasks_count: int
    force_last_assignment: bool
    force_last_assignment_delay_seconds: int
    mix_tasks_in_creation_order: bool
    shuffle_tasks_in_task_suite: bool
    golden_task_distribution_function: TaskDistributionFunction
    training_task_distribution_function: TaskDistributionFunction
