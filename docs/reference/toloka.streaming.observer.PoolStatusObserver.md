# PoolStatusObserver
`toloka.streaming.observer.PoolStatusObserver`

```
PoolStatusObserver(
    self,
    toloka_client: Union[TolokaClient, ...],
    pool_id: str
)
```

Observer for pool status change.


For usage with Pipeline.

Allow to register callbacks using the following methods:
    * on_open
    * on_closed
    * on_archieved
    * on_locked
    * on_status_change

The Pool object will be passed to the triggered callbacks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**...**|<p>TolokaClient instance or async wrapper around it.</p>
`pool_id`|**str**|<p>Pool ID.</p>

**Examples:**

Bind to the pool's close to make some aggregations.

```python
def call_this_on_close(pool: Pool) -> None:
    assignments = client.get_assignments_df(pool_id=pool.id, status=['APPROVED'])
    do_some_aggregation(assignments)
observer = PoolStatusObserver(toloka_client, pool_id='123')
observer.on_close(call_this_on_close)
```

Call something at any status change.

```python
observer.on_status_change(lambda pool: ...)
```
## Methods summary

| Method | Description |
| :------| :-----------|
[on_archieved](toloka.streaming.observer.PoolStatusObserver.on_archieved.md)| None
[on_closed](toloka.streaming.observer.PoolStatusObserver.on_closed.md)| None
[on_locked](toloka.streaming.observer.PoolStatusObserver.on_locked.md)| None
[on_open](toloka.streaming.observer.PoolStatusObserver.on_open.md)| None
[on_status_change](toloka.streaming.observer.PoolStatusObserver.on_status_change.md)| None
[register_callback](toloka.streaming.observer.PoolStatusObserver.register_callback.md)| Register given callable for pool status change to given value.
