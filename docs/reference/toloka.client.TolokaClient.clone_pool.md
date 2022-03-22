# clone_pool
`toloka.client.TolokaClient.clone_pool` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
clone_pool(self, pool_id: str)
```

Duplicates existing pool


An empty pool with the same parameters will be created.
A new pool will be attached to the same project.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the existing pool.</p>

* **Returns:**

  New pool.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

```python
toloka_client.clone_pool(pool_id='1')
```
