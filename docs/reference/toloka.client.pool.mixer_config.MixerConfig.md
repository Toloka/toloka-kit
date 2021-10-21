# MixerConfig
`toloka.client.pool.mixer_config.MixerConfig`

```
MixerConfig(
    self,
    *,
    real_tasks_count: int = 0,
    golden_tasks_count: int = 0,
    training_tasks_count: int = 0,
    min_real_tasks_count: Optional[int] = None,
    min_golden_tasks_count: Optional[int] = None,
    min_training_tasks_count: Optional[int] = None,
    force_last_assignment: Optional[bool] = None,
    force_last_assignment_delay_seconds: Optional[int] = None,
    mix_tasks_in_creation_order: Optional[bool] = None,
    shuffle_tasks_in_task_suite: Optional[bool] = None,
    golden_task_distribution_function: Optional[TaskDistributionFunction] = None,
    training_task_distribution_function: Optional[TaskDistributionFunction] = None
)
```

Parameters for automatically creating a task suite ("smart mixing").


For more information about creating task see Yandex.Toloka Requester's guide.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`real_tasks_count`|**int**|<p>The number of main tasks to put in a task suite. The maximum number of tasks in a task suite if training_task_distribution_function or golden_task_distribution_function are used.</p>
`golden_tasks_count`|**int**|<p>The number of control (&quot;golden set&quot;) tasks to put in a task suite.</p>
`training_tasks_count`|**int**|<p>The number of training tasks to put in a task suite.</p>
`min_real_tasks_count`|**Optional\[int\]**|<p>Minimum number of main tasks in a task suite (if the number of assignments left is less than the one specified in real_tasks_count). Minimum — 0. By default, the value is the same as in real_tasks_count.</p>
`min_golden_tasks_count`|**Optional\[int\]**|<p>Minimum number of control tasks in a task suite (if the number of assignments left is less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same as in golden_tasks_count.</p>
`min_training_tasks_count`|**Optional\[int\]**|<p>Minimum number of training tasks in a task suite (if the number of assignments left is less than the one specified in golden_tasks_count). Minimum — 0. By default, the value is the same as in training_tasks_count.</p>
`force_last_assignment`|**Optional\[bool\]**|<p>Setup for the last set of tasks in the pool, if less than the minimum remaining number of tasks are not completed (mixer_config.min_real_tasks_count). Values:<ul><li>true - issue an incomplete task set.</li><li>false - don&#x27;t issue tasks. This option can be used if you are adding tasks after the pool is started. This parameter only applies to main tasks. The number of control and training tasks in the last set must be complete (golden_tasks_count, training_tasks_count).</li></ul></p>
`force_last_assignment_delay_seconds`|**Optional\[int\]**|<p>Waiting time (in seconds) since the addition of the task, or increase in the overlap, prior to the issuance of the last set of tasks in the pool. The minimum is 0, the maximum is 86,400 seconds (one day). This parameter can be used if the pool has force_last_assignment: True.</p>
`mix_tasks_in_creation_order`|**Optional\[bool\]**|<p>The order for including tasks in suites:<ul><li>True — Add tasks to suites in the order in which they were uploaded. For example, in a pool with an     overlap of 5, the first uploaded task will be included in the first 5 task suites. They will be     assigned to 5 users.</li><li>False — Add tasks to suites in random order.</li></ul></p>
`shuffle_tasks_in_task_suite`|**Optional\[bool\]**|<p>The order of tasks within a suite:<ul><li>True — Random.</li><li>False — The order in which tasks were uploaded.</li></ul></p>
`golden_task_distribution_function`|**Optional\[[TaskDistributionFunction](toloka.client.task_distribution_function.TaskDistributionFunction.md)\]**|<p>Issue of control tasks with uneven frequency. The option allows you to change the frequency of checking as the user completes more tasks.</p>
`training_task_distribution_function`|**Optional\[[TaskDistributionFunction](toloka.client.task_distribution_function.TaskDistributionFunction.md)\]**|<p>Issue of training tasks with uneven frequency. The option allows you to change the frequency of training tasks as the user completes more tasks.</p>
