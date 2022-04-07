# TaskSuiteSortItems
`toloka.client.search_requests.TaskSuiteSortItems`

```python
TaskSuiteSortItems(self, items=None)
```

Parameters for sorting task suite search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.TaskSuiteSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Task set ID (in ascending order).</li><li>created - Date of creation of the set of tasks in UTC in the format YYYY-MM-DD (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.TaskSuiteSortItems(['-created', 'id'])
result = toloka_client.find_task_suites(pool_id=my_pretty_pool_id, sort=sort, limit=10)
```
