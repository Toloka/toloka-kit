# AppBatchSortItems
`toloka.client.search_requests.AppBatchSortItems`

```python
AppBatchSortItems(self, items=None)
```

Parameters for sorting App batch search results.


You can specify multiple parameters separated by a comma. To change the sorting direction to descending, add the
minus sign before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.AppBatchSortItems.SortItem.md)\]\]**|<p>The order and direction of sorting the results. Available parameters:<ul><li>id - by id;</li><li>name - by name;</li><li>created — by creation date. The date is specified in UTC in the YYYY-MM-DD format.</li></ul></p>
