# SkillSortItems
`toloka.client.search_requests.SkillSortItems`

```python
SkillSortItems(self, items=None)
```

Parameters for sorting skill search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.SkillSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Skill ID in ascending order.</li><li>created - Skill creation date in UTC in yyyy-MM-DD format (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.SkillSortItems(['-created', 'id'])
result = toloka_client.find_skills(name='Image annotation', sort=sort, limit=10)
```
