# update_pool
`toloka.client.TolokaClient.update_pool`

```python
update_pool(
    self,
    pool_id: str,
    pool: Pool
)
```

Makes changes to the pool

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be changed.</p>
`pool`|**[Pool](toloka.client.pool.Pool.md)**|<p>A pool object with all the fields: those that will be updated and those that will not.</p>

* **Returns:**

  Pool object with all fields.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

```python
updated_pool = toloka_client.update_pool(pool_id=old_pool_id, pool=new_pool_object)
```
