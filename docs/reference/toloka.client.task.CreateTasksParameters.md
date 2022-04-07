# CreateTasksParameters
`toloka.client.task.CreateTasksParameters` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/task.py#L133)

```python
CreateTasksParameters(
    self,
    *,
    allow_defaults: Optional[bool] = None,
    open_pool: Optional[bool] = None,
    skip_invalid_items: Optional[bool] = None,
    operation_id: Optional[UUID] = None,
    async_mode: Optional[bool] = True
)
```

Parameters for Tasks creation controlling


Used when creating many Tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`allow_defaults`|**Optional\[bool\]**|<p>Overlap setting:<ul><li>True — Use the overlap value that is set in the `defaults.default_overlap_for_new_task_suites` pool parameter.</li><li>False — Use the overlap value that is set in the `overlap` task suite parameter.</li></ul></p>
`open_pool`|**Optional\[bool\]**|<p>Open the pool immediately after creating a task suite, if the pool is closed.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Task validation option:<ul><li>True — All valid tasks are added. If a task does not pass validation, then it is not added to Toloka. All such tasks are listed in the response.</li><li>False — If any task does not pass validation, then operation is cancelled and no tasks are added to Toloka.</li></ul></p>
`async_mode`|**Optional\[bool\]**|<p>Request processing mode:<ul><li>True — Asynchronous operation is started internally and `create_tasks` waits for the completion of it. It is recommended to create no more than 10,000 tasks per request in this mode.</li><li>False — The request is processed synchronously. A maximum of 5000 tasks can be added in a single request in this mode.</li></ul></p>
