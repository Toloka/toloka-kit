# patch_task
`toloka.client.TolokaClient.patch_task`

Changes a task overlap value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**str**|<p>The ID of the task.</p>
`overlap`|**Optional\[int\]**|<p>Overlap value.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Infinite overlap:<ul><li>True — Assign the task to all users. It is useful for training tasks.</li><li>False — Overlap value specified for the task or for the pool is used. </li></ul></p><p>Default value: False.</p>
`baseline_solutions`|**Optional\[List\[[Task.BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p></p>

* **Returns:**

  The task with updated fields.

* **Return type:**

  [Task](toloka.client.task.Task.md)
