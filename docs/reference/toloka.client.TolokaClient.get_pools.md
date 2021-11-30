# get_pools
`toloka.client.TolokaClient.get_pools`

Finds all pools that match certain rules and returns them in an iterable object


Unlike find_pools, returns generator. Does not sort pools.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status`|**Optional\[[Pool.Status](toloka.client.pool.Pool.Status.md)\]**|<p>Pool status<ul><li>OPEN</li><li>CLOSED</li><li>ARCHIVED</li><li>LOCKED</li></ul></p>
`project_id`|**Optional\[str\]**|<p>ID of the project to which the pool is attached.</p>
`id_lt`|**Optional\[str\]**|<p>Pools with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Pools with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Pools with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Pools with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Pools created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Pools created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Pools created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Pools created after or on the specified date.</p>
`last_started_lt`|**Optional\[datetime\]**|<p>Pools that were last opened before the specified date.</p>
`last_started_lte`|**Optional\[datetime\]**|<p>Pools that were last opened on or before the specified date.</p>
`last_started_gt`|**Optional\[datetime\]**|<p>Pools that were last opened after the specified date.</p>
`last_started_gte`|**Optional\[datetime\]**|<p>Pools that were last opened on or after the specified date.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Pool](toloka.client.pool.Pool.md), None, None\]

**Examples:**

How to get all open pools from project.

```python
open_pools = toloka_client.get_pools(project_id='1', status='OPEN')
```

How to get all pools from project.

```python
all_pools = toloka_client.get_pools(project_id='1')
```
