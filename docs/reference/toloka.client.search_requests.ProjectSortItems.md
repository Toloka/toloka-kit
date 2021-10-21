# ProjectSortItems
`toloka.client.search_requests.ProjectSortItems`

```
ProjectSortItems(self, items=None)
```

Parameters for sorting project search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Project ID in ascending order.</li><li>created - Project creation date in UTC in yyyy-MM-DD format (ascending).</li><li>public_name - Project name (in alphabetical order).</li><li>private_comment - Comment on the project (in alphabetical order).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.ProjectSortItems(['-public_name', 'id'])
result = toloka_client.find_projects(status='ACTIVE', sort=sort, limit=50)
```
