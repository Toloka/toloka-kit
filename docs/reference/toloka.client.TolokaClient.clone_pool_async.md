# clone_pool_async
`toloka.client.TolokaClient.clone_pool_async`

```
clone_pool_async(self, pool_id: str)
```

Duplicates existing pool, asynchronous version


An empty pool with the same parameters will be created.
A new pool will be attached to the same project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the existing pool.</p>

* **Returns:**

  An operation upon completion of which you can get the new pool.

* **Return type:**

  [PoolCloneOperation](toloka.client.operations.PoolCloneOperation.md)

**Examples:**

```python
new_pool = toloka_client.clone_pool_async(pool_id='1')
toloka_client.wait_operation(new_pool)
```
