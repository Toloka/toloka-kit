# register_callback
`toloka.streaming.observer.AssignmentsObserver.register_callback` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/observer.py#L323)

```python
register_callback(
    self,
    callback: Union[Callable[[List[AssignmentEvent]], None], Callable[[List[AssignmentEvent]], Awaitable[None]]],
    event_type: AssignmentEvent.Type
)
```

Register given callable for given event type.


Callback will be called multiple times if it has been registered for multiple event types.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`callback`|**Union\[Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], None\], Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], Awaitable\[None\]\]\]**|<p>Sync or async callable that pass List[AssignmentEvent] of desired event type.</p>
`event_type`|**[AssignmentEvent.Type](toloka.streaming.event.AssignmentEvent.Type.md)**|<p>Selected event type.</p>

* **Returns:**

  The same callable passed as callback.

* **Return type:**

  Union\[Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], None\], Callable\[\[List\[[AssignmentEvent](toloka.streaming.event.AssignmentEvent.md)\]\], Awaitable\[None\]\]\]
