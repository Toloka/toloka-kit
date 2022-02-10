# PoolSortItems
`toloka.client.search_requests.PoolSortItems`

```python
PoolSortItems(self, items=None)
```

Parameters for sorting pool search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.PoolSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Pool ID in ascending order.</li><li>created - Pool creation date in UTC in yyyy-MM-DD format (ascending).</li><li>last_started - The date the pool was last started (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.PoolSortItems(['-last_started', 'id'])
result = toloka_client.find_pools(status='OPEN', sort=sort, limit=50)
```
