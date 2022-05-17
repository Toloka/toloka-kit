# TaskPatch
`toloka.client.task.TaskPatch` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/task.py#L167)

```python
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
`overlap`|**Optional\[int\]**|<p>Overlap value.</p>
`infinite_overlap`|**Optional\[bool\]**|<p>Infinite overlap:<ul><li>True — Assign the task to all users. It is useful for training tasks.</li><li>False — Overlap value specified for the task or for the pool is used. </li></ul></p><p>Default value: False.</p>
`baseline_solutions`|**Optional\[List\[[Task.BaselineSolution](toloka.client.task.Task.BaselineSolution.md)\]\]**|<p></p>
