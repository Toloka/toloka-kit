# register_callback
`toloka.streaming.observer.AssignmentsObserver.register_callback`

```python
register_callback(
    self,
    callback: Union[Callable[[List[AssignmentEvent]], None], Callable[[List[AssignmentEvent]], Awaitable[None]]],
    event_type: Union[AssignmentEvent.Type, str]
)
```

Register given callable for given event type.


Callback will be called multiple times if it has been registered for multiple event types.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`callback`|**Union\[Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], None\], Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], Awaitable\[None\]\]\]**|<p>Sync or async callable that pass List[AssignmentEvent] of desired event type.</p>
`event_type`|**Union\[[AssignmentEvent.Type](toloka.streaming.event.AssignmentEvent.Type.md), str\]**|<p>Selected event type.</p>

* **Returns:**

  The same callable passed as callback.

* **Return type:**

  Union\[Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], None\], Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], Awaitable\[None\]\]\]
