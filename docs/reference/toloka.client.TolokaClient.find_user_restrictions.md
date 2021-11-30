# find_user_restrictions
`toloka.client.TolokaClient.find_user_restrictions`

Finds all user restrictions that match certain rules


As a result, it returns an object that contains the first part of the found user restrictions and whether there
are any more results.
It is better to use the "get_user_restriction" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scope`|**Optional\[[UserRestriction.Scope](toloka.client.user_restriction.UserRestriction.Scope.md)\]**|<p>The scope of the ban<ul><li>ALL_PROJECTS</li><li>PROJECT</li><li>POOL</li></ul></p>
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`project_id`|**Optional\[str\]**|<p>The ID of the project that is blocked.</p>
`pool_id`|**Optional\[str\]**|<p>The ID of the pool that is blocked.</p>
`id_lt`|**Optional\[str\]**|<p>Bans with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Bans with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Bans with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Bans with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Bans created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Bans created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Bans created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Bans created after or on the specified date.</p>
`sort`|**Union\[List\[str\], [UserRestrictionSortItems](toloka.client.search_requests.UserRestrictionSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned.</p>

* **Returns:**

  The first `limit` user restrictions in `items`.
And a mark that there is more.

* **Return type:**

  [UserRestrictionSearchResult](toloka.client.search_results.UserRestrictionSearchResult.md)

**Examples:**

```python
toloka_client.find_user_restrictions(sort=['-created', '-id'], limit=10)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
