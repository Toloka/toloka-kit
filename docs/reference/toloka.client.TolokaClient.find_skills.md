# find_skills
`toloka.client.TolokaClient.find_skills`

Finds all skills that match certain rules


As a result, it returns an object that contains the first part of the found skills and whether there
are any more results.
It is better to use the "get_skills" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>Skill name.</p>
`id_lt`|**Optional\[str\]**|<p>Skills with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Skills with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Skills with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Skills with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Skills created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Skills created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Skills created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Skills created on or after the specified date.</p>
`sort`|**Union\[List\[str\], [SkillSortItems](toloka.client.search_requests.SkillSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned.</p>

* **Returns:**

  The first `limit` skills in `items`.
And a mark that there is more.

* **Return type:**

  [SkillSearchResult](toloka.client.search_results.SkillSearchResult.md)

**Examples:**

Find ten most recently created skills.

```python
toloka_client.find_skills(sort=['-created', '-id'], limit=10)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
