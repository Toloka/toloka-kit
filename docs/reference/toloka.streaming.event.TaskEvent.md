# TaskEvent
`toloka.streaming.event.TaskEvent` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/event.py#L55)

```python
TaskEvent(
    self,
    *,
    event_time: Optional[datetime] = None,
    task: Optional[Task] = None
)
```

Task-related event.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`event_time`|**Optional\[datetime\]**|<p>Event datetime.</p>
`task`|**Optional\[[Task](toloka.client.task.Task.md)\]**|<p>Task object itself.</p>
