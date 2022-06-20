# UserSkillSortItems
`toloka.client.search_requests.UserSkillSortItems`

```python
UserSkillSortItems(self, items=None)
```

Parameters for sorting user skill search results


You can specify multiple parameters.
To change the sorting direction (sort in descending order), add a hyphen before the parameter. For example, sort=-id.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[SortItem](toloka.client.search_requests.UserSkillSortItems.SortItem.md)\]\]**|<p>Fields by which to sort. Possible values:<ul><li>id - Skill ID in ascending order.</li><li>created - Date the skill was created in UTC in the yyyy-MM-DD format (ascending).</li><li>modified - Date the skill was modified in UTC in the yyyy-MM-DD format (ascending).</li></ul></p>

**Examples:**

How to specify and use SortItems.

```python
sort = toloka.client.search_requests.UserSkillSortItems(['-created', 'id'])
result = toloka_client.find_user_skills(skill_id=my_useful_skill_id, sort=sort, limit=10)
```
