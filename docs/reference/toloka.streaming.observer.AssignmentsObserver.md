# AssignmentsObserver
`toloka.streaming.observer.AssignmentsObserver`

```python
AssignmentsObserver(
    self,
    toloka_client: Union[TolokaClient, AsyncMultithreadWrapper[TolokaClient]],
    pool_id: str,
    *,
    name: Optional[str] = None
)
```

Observer for the pool's assignment events.


For usage with Pipeline.

Allow to register callbacks using the following methods:
    * on_created
    * on_submitted
    * on_accepted
    * on_rejected
    * on_skipped
    * on_expired

Corresponding assignment events will be passed to the triggered callbacks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**[AsyncInterfaceWrapper](toloka.util.async_utils.AsyncInterfaceWrapper.md)\[Union\[[TolokaClient](toloka.client.TolokaClient.md), [AsyncMultithreadWrapper](toloka.util.async_utils.AsyncMultithreadWrapper.md)\[[TolokaClient](toloka.client.TolokaClient.md)\]\]\]**|<p>TolokaClient instance or async wrapper around it.</p>
`pool_id`|**str**|<p>Pool ID.</p>

**Examples:**

Send submitted assignments for verification.

```python
def handle_submitted(evets: List[AssignmentEvent]) -> None:
    verification_tasks = [create_veridication_task(item.assignment) for item in evets]
    toloka_client.create_tasks(verification_tasks, open_pool=True)
observer = AssignmentsObserver(toloka_client, pool_id='123')
observer.on_submitted(handle_submitted)
```
## Methods summary

| Method | Description |
| :------| :-----------|
[inject](toloka.streaming.observer.AssignmentsObserver.inject.md)| None
[on_accepted](toloka.streaming.observer.AssignmentsObserver.on_accepted.md)| None
[on_any_event](toloka.streaming.observer.AssignmentsObserver.on_any_event.md)| None
[on_created](toloka.streaming.observer.AssignmentsObserver.on_created.md)| None
[on_expired](toloka.streaming.observer.AssignmentsObserver.on_expired.md)| None
[on_rejected](toloka.streaming.observer.AssignmentsObserver.on_rejected.md)| None
[on_skipped](toloka.streaming.observer.AssignmentsObserver.on_skipped.md)| None
[on_submitted](toloka.streaming.observer.AssignmentsObserver.on_submitted.md)| None
[register_callback](toloka.streaming.observer.AssignmentsObserver.register_callback.md)| Register given callable for given event type.
