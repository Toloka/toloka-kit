# archive_pool_async
`toloka.client.TolokaClient.archive_pool_async`

```python
archive_pool_async(self, pool_id: str)
```

Sends pool to archive, asynchronous version


The pool must be in the status "closed".
The archived pool is not deleted. You can access it when you will need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of pool that will be archived.</p>

* **Returns:**

  An operation upon completion of which you can get the pool with updated status. If
pool is already archived then None is returned

* **Return type:**

  Optional\[[PoolArchiveOperation](toloka.client.operations.PoolArchiveOperation.md)\]

**Examples:**

```python
closed_pool = next(toloka_client.get_pools(status='CLOSED'))
archive_op = toloka_client.archive_pool_async(pool_id=closed_pool.id)
toloka_client.wait_operation(archive_op)
```
