# UserBonusSortItems
`toloka.client.search_requests.UserBonusSortItems`

```
UserBonusSortItems(self, items=None)
```

Parameters for sorting user bonus search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.UserBonusSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Bonus ID in ascending order.</li><li>created - Creation date in UTC format yyyy-MM-DD (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.UserBonusSortItems(['-created', 'id'])
result = toloka_client.find_user_bonuses(user_id=best_performer_id, sort=sort, limit=10)
```
