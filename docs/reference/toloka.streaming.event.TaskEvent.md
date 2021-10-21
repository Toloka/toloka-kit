# TaskEvent
`toloka.streaming.event.TaskEvent`

```
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
