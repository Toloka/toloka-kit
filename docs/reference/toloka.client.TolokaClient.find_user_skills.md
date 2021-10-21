# find_user_skills
`toloka.client.TolokaClient.find_user_skills`

Finds all user skills that match certain rules


UserSkill describe the skill value for a specific performer.
As a result, it returns an object that contains the first part of the found user skills and whether there
are any more results.
It is better to use the "get_user_skills" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`skill_id`|**Optional\[str\]**|<p>Skill ID.</p>
`id_lt`|**Optional\[str\]**|<p>Skills with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Skills with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Skills with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Skills with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Skills created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Skills created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Skills created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Skills created on or after the specified date.</p>
`modified_lt`|**Optional\[datetime\]**|<p>Skills that changed before the specified date.</p>
`modified_lte`|**Optional\[datetime\]**|<p>Skills that changed before the specified date.</p>
`modified_gt`|**Optional\[datetime\]**|<p>Skills changed after the specified date.</p>
`modified_gte`|**Optional\[datetime\]**|<p>Skills created on or after the specified date.</p>
`sort`|**Union\[List\[str\], [UserSkillSortItems](toloka.client.search_requests.UserSkillSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned.</p>

* **Returns:**

  The first `limit` user skills in `items`.
And a mark that there is more.

* **Return type:**

  [UserSkillSearchResult](toloka.client.search_results.UserSkillSearchResult.md)

**Examples:**

```python
toloka_client.find_user_skills(limit=10)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
