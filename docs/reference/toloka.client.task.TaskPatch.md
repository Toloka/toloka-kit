# TaskPatch
`toloka.client.task.TaskPatch`

```
TaskPatch(
    self,
    *,
    overlap: Optional[int] = None,
    infinite_overlap: Optional[bool] = None,
    baseline_solutions: Optional[List[Task.BaselineSolution]] = None
)
```

Parameters for changing overlap or baseline_solutions of a specific Task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`overlap`|**Optional\[int\]**|<p>Overlapping a set of tasks.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Issue a task with infinite overlap. Used, for example, for sets of training tasks to give them to all users:<ul><li>True - Set infinite overlap.</li><li>False - Leave the overlap specified for the task or pool. Default Behaviour.</li></ul></p>
`baseline_solutions`|**Optional\[List\[[Task.BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p></p>
