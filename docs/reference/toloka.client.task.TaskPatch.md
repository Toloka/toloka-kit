# TaskPatch
`toloka.client.task.TaskPatch` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/task.py#L168)

```python
TaskPatch(
    self,
    *,
    overlap: Optional[int] = None,
    infinite_overlap: Optional[bool] = None,
    baseline_solutions: Optional[List[Task.BaselineSolution]] = None,
    known_solutions: Optional[List[BaseTask.KnownSolution]] = None,
    message_on_unknown_solution: Optional[str] = None
)
```

Parameters for changing overlap or baseline_solutions of a specific Task

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`overlap`|**Optional\[int\]**|<p>Overlap value.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Infinite overlap:<ul><li>True — Assign the task to all users. It is useful for training tasks.</li><li>False — Overlap value specified for the task or for the pool is used. </li></ul></p><p>Default value: False.</p>
`baseline_solutions`|**Optional\[List\[[Task.BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p>Preliminary responses. This data simulates performer responses when calculating confidence in a response. It is used in dynamic overlap (also known as incremental relabeling or IRL) and aggregation of results by skill.</p>
`known_solutions`|**Optional\[List\[[BaseTask.KnownSolution](toloka.client.task.BaseTask.KnownSolution.md)\]\]**|<p>Responses and hints for control tasks and training tasks. If multiple output fields are included in the validation, all combinations of the correct response must be specified.</p>
`message_on_unknown_solution`|**Optional\[str\]**|<p>Hint for the task (for training tasks).</p>
