# Pipeline
`toloka.streaming.pipeline.Pipeline`

```
Pipeline(self, period: timedelta = ...)
```

An entry point for toloka streaming pipelines.


Allow you to register multiple observers and call them periodically
while at least one of them may resume.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`period`|**timedelta**|<p>Period of observers calls. By default, 60 seconds.</p>

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
## Methods summary

| Method | Description |
| :------| :-----------|
[register](toloka.streaming.pipeline.Pipeline.register.md)| Register given observer.
[run](toloka.streaming.pipeline.Pipeline.run.md)| None
