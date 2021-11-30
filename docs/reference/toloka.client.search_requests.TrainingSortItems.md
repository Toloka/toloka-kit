# TrainingSortItems
`toloka.client.search_requests.TrainingSortItems`

```
TrainingSortItems(self, items=None)
```

Parameters for sorting training pool search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.TrainingSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Training pool ID in ascending order.</li><li>created - Training pool creation date in UTC in yyyy-MM-DD format (ascending).</li><li>last_started - The date the pool was last started (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.TrainingSortItems(['-last_started', 'id'])
result = toloka_client.find_trainings(status='OPEN', sort=sort, limit=50)
```
