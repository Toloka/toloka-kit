# get_pool
`toloka.client.TolokaClient.get_pool` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

```python
get_pool(self, pool_id: str)
```

Reads one specific pool

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`pool_id`|**str**|<p>ID of the pool.</p>

* **Returns:**

  The pool.

* **Return type:**

  [Pool](toloka.client.pool.Pool.md)

**Examples:**

```python
toloka_client.get_pool(pool_id='1')
```
