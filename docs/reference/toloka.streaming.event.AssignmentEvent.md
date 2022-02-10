# AssignmentEvent
`toloka.streaming.event.AssignmentEvent`

```python
AssignmentEvent(
    self,
    *,
    event_time: Optional[datetime] = None,
    event_type: Union[Type, str, None] = None,
    assignment: Optional[Assignment] = None
)
```

Assignment-related event.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`event_time`|**Optional\[datetime\]**|<p>Event datetime.</p>
`event_type`|**Optional\[[Type](toloka.streaming.event.AssignmentEvent.Type.md)\]**|<p>One of the folllowing event types:<ul><li>CREATED</li><li>SUBMITTED</li><li>ACCEPTED</li><li>REJECTED</li><li>SKIPPED</li><li>EXPIRED</li></ul></p>
`assignment`|**Optional\[[Assignment](toloka.client.assignment.Assignment.md)\]**|<p>Assignment object itself.</p>
