# find_pools
`toloka.client.TolokaClient.find_pools`

Finds all pools that match certain rules


As a result, it returns an object that contains the first part of the found pools and whether there
are any more results.
It is better to use the "get_pools" method, they allow to iterate trought all results
and not just the first output.

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
`sort`|**Union\[List\[str\], [PoolSortItems](toloka.client.search_requests.PoolSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned. The maximum is 300. Defaults to None, in which case it returns first 20 results.</p>

* **Returns:**

  The first `limit` pools in `items`.
And a mark that there is more.

* **Return type:**

  [PoolSearchResult](toloka.client.search_results.PoolSearchResult.md)

**Examples:**

Find all pools in all projects.

```python
toloka_client.find_pools()
```

Find all open pools in all projects.

```python
toloka_client.find_pools(status='OPEN')
```

Find open pools in a specific project.

```python
toloka_client.find_pools(status='OPEN', project_id='1')
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an
indicator `has_more=True`.
