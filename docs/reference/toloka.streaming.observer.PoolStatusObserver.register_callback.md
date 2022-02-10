# register_callback
`toloka.streaming.observer.PoolStatusObserver.register_callback`

```python
register_callback(
    self,
    callback: Union[Callable[[Pool], None], Callable[[Pool], Awaitable[None]]],
    changed_to: Union[Pool.Status, str]
)
```

Register given callable for pool status change to given value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`callback`|**Union\[Callable\[\[[Pool](toloka.client.pool.Pool.md)\], None\], Callable\[\[[Pool](toloka.client.pool.Pool.md)\], Awaitable\[None\]\]\]**|<p>Sync or async callable that pass Pool object.</p>
`changed_to`|**Union\[[Pool.Status](toloka.client.pool.Pool.Status.md), str\]**|<p>Pool status value to register for.</p>

* **Returns:**

  The same callable passed as callback.

* **Return type:**

  Union\[Callable\[\[[Pool](toloka.client.pool.Pool.md)\], None\], Callable\[\[[Pool](toloka.client.pool.Pool.md)\], Awaitable\[None\]\]\]
