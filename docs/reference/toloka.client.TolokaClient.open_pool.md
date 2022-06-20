# open_pool
`toloka.client.TolokaClient.open_pool` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

```python
open_pool(self, pool_id: str)
```

Starts distributing tasks from the pool


Performers will see your tasks only after that call.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool that will be started.</p>

* **Returns:**

  Pool object with new status.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

Open the pool for performers.

```python
toloka_client.open_pool(pool_id='1')
```
