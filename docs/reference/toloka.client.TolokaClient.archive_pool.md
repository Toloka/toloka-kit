# archive_pool
`toloka.client.TolokaClient.archive_pool`

```
archive_pool(self, pool_id: str)
```

Sends pool to archive


The pool must be in the status "closed".
The archived pool is not deleted. You can access it when you will need it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of pool that will be archived.</p>

* **Returns:**

  Object with updated status.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

```python
closed_pool = next(toloka_client.get_pools(status='CLOSED'))
toloka_client.archive_pool(pool_id=closed_pool.id)
```
