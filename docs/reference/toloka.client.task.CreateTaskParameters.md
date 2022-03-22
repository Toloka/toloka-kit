# CreateTaskParameters
`toloka.client.task.CreateTaskParameters` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/task.py#L112)

```python
CreateTaskParameters(
    self,
    *,
    allow_defaults: Optional[bool] = None,
    open_pool: Optional[bool] = None
)
```

Parameters for Task creation controlling


Used when creating one Task.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`allow_defaults`|**Optional\[bool\]**|<p>Overlap settings:<ul><li>True - Use the overlap that is set in the pool parameters (in the defaults.default_overlap_for_new_task_suites key).</li><li>False - Use the overlap that is set in the task suite parameters (in the overlap field).</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
