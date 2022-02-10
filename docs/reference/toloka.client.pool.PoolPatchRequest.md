# PoolPatchRequest
`toloka.client.pool.PoolPatchRequest`

```python
PoolPatchRequest(self, priority: Optional[int] = None)
```

Class for changing the priority of the pool issue


To do this use TolokaClient.patch_pool(). You can use expanded version, then pass "priority" directly to "patch_pool".

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`priority`|**Optional\[int\]**|<p>The priority of the pool in relation to other pools in the project with the same task price and set of filters. Users are assigned tasks with a higher priority first. Possible values: from -100 to 100.</p>

**Examples:**

How to set highest priority to some pool.

```python
toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
patched_pool = toloka_client.patch_pool(existing_pool_id, 100)
print(patched_pool.priority)
```
