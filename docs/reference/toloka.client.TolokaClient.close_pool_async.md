# close_pool_async
`toloka.client.TolokaClient.close_pool_async` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
close_pool_async(self, pool_id: str)
```

Stops distributing tasks from the pool, asynchronous version


If all tasks done, the pool will be closed automatically.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be closed.</p>

* **Returns:**

  An operation upon completion of which you can get the pool with updated
status. If pool is already closed then None is returned.

* **Return type:**

  Optional\[[PoolCloseOperation](toloka.client.operations.PoolCloseOperation.md)\]

**Examples:**

```python
open_pool = next(toloka_client.get_pools(status='OPEN'))
close_op = toloka_client.close_pool_async(pool_id=open_pool.id)
toloka_client.wait_operation(close_op)
```
