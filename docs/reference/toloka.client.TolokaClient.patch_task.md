# patch_task
`toloka.client.TolokaClient.patch_task`

Changes the task overlap

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`task_id`|**str**|<p>ID of the task that will be changed.</p>
`overlap`|**Optional\[int\]**|<p>Overlapping a set of tasks.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Issue a task with infinite overlap. Used, for example, for sets of training tasks to give them to all users:<ul><li>True - Set infinite overlap.</li><li>False - Leave the overlap specified for the task or pool. Default Behaviour.</li></ul></p>
`baseline_solutions`|**Optional\[List\[[Task.BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p></p>

* **Returns:**

  Task with updated fields.

* **Return type:**

  [Task](toloka.client.task.Task.md)
