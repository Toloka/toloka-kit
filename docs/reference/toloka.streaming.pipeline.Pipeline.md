# Pipeline
`toloka.streaming.pipeline.Pipeline` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/streaming/pipeline.py#L65)

```python
Pipeline(
    self,
    period: timedelta = ...,
    storage: Optional[BaseStorage] = None,
    *,
    name: Optional[str] = None
)
```

An entry point for toloka streaming pipelines.


Allow you to register multiple observers and call them periodically
while at least one of them may resume.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`period`|**timedelta**|<p>Period of observers calls. By default, 60 seconds.</p>
`storage`|**Optional\[[BaseStorage](toloka.streaming.storage.BaseStorage.md)\]**|<p>Optional storage object to save pipeline&#x27;s state. Allow to recover from previous state in case of failure.</p>

**Examples:**

Get assignments from segmentation pool and send them for verification to another pool.

```python
def handle_submitted(events: List[AssignmentEvent]) -> None:
    verification_tasks = [create_verification_task(item.assignment) for item in events]
    toloka_client.create_tasks(verification_tasks, open_pool=True)
def handle_accepted(events: List[AssignmentEvent]) -> None:
    do_some_aggregation([item.assignment for item in events])
async_toloka_client = AsyncMultithreadWrapper(toloka_client)
observer_123 = AssignmentsObserver(async_toloka_client, pool_id='123')
observer_123.on_submitted(handle_submitted)
observer_456 = AssignmentsObserver(async_toloka_client, pool_id='456')
observer_456.on_accepted(handle_accepted)
pipeline = Pipeline()
pipeline.register(observer_123)
pipeline.register(observer_456)
await pipeline.run()
```

One-liners version.

```python
pipeline = Pipeline()
pipeline.register(AssignmentsObserver(toloka_client, pool_id='123')).on_submitted(handle_submitted)
pipeline.register(AssignmentsObserver(toloka_client, pool_id='456')).on_accepted(handle_accepted)
await pipeline.run()
```

With external storage.

```python
from toloka.streaming import S3Storage, ZooKeeperLocker
locker = ZooKeeperLocker(...)
storage = S3Storage(locker=locker, ...)
pipeline = Pipeline(storage=storage)
await pipeline.run()  # Save state after each iteration. Try to load saved at start.
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[observers_iter](toloka.streaming.pipeline.Pipeline.observers_iter.md)| Iterate over registered observers.
[register](toloka.streaming.pipeline.Pipeline.register.md)| Register given observer.
[run](toloka.streaming.pipeline.Pipeline.run.md)| None
