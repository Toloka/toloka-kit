# patch_pool
`toloka.client.TolokaClient.patch_pool`

Changes the priority of the pool issue

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be patched.</p>
`priority`|**Optional\[int\]**|<p>The priority of the pool in relation to other pools in the project with the same task price and set of filters. Users are assigned tasks with a higher priority first. Possible values: from -100 to 100.</p>

* **Returns:**

  Object with updated priority.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

Set the highest priority to a specified pool.

```python
toloka_client.patch_pool(pool_id='1', priority=100)
```
