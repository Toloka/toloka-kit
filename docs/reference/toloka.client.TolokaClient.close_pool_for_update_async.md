# close_pool_for_update_async
`toloka.client.TolokaClient.close_pool_for_update_async` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
close_pool_for_update_async(self, pool_id: str)
```

Closes pool for update, asynchronous version

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be closed for update.</p>

* **Returns:**

  An operation upon completion of which you can get the pool with updated
status. If pool is already closed for update then None is returned.

* **Return type:**

  Optional\[[PoolCloseOperation](toloka.client.operations.PoolCloseOperation.md)\]

**Examples:**

```python
close_op = toloka_client.close_pool_for_update_async(pool_id='1')
toloka_client.wait_operation(close_op)
```
