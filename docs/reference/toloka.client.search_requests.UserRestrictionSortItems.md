# UserRestrictionSortItems
`toloka.client.search_requests.UserRestrictionSortItems`

```
UserRestrictionSortItems(self, items=None)
```

Parameters for sorting user restriction search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - User restriction ID in ascending order.</li><li>created - Creation date in UTC format yyyy-MM-DD (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.UserRestrictionSortItems(['-created', 'id'])
result = toloka_client.find_user_restrictions(pool_id=my_pretty_pool_id, sort=sort, limit=10)
```
