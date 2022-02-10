# close_pool_for_update
`toloka.client.TolokaClient.close_pool_for_update`

```python
close_pool_for_update(self, pool_id: str)
```

Closes pool for update

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be closed for update.</p>

* **Returns:**

  Pool object with new status.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

```python
toloka_client.close_pool_for_update(pool_id='1')
```
