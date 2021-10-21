# AssignmentSortItems
`toloka.client.search_requests.AssignmentSortItems`

```
AssignmentSortItems(self, items=None)
```

Parameters for sorting assignment search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - ID for issuing a set of tasks (in ascending order).</li><li>created - Date of issue of the set of tasks in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li><li>submitted - Date of completion of the set of tasks in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li><li>accepted - Date the set of tasks was accepted in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li><li>rejected - Date the set of tasks was rejected in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li><li>skipped - Date the set of tasks was skipped in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li><li>expired - Date the set of tasks was expired in UTC in ISO 8601 format YYYY-MM-DDThh:mm:ss[.sss] (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.AssignmentSortItems(['-submitted', 'id'])
result = toloka_client.find_assignments(status='SUBMITTED', sort=sort, limit=10)
```
