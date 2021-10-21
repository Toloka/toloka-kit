# get_user_restrictions
`toloka.client.TolokaClient.get_user_restrictions`

Finds all user restrictions that match certain rules and returns them in an iterable object


Unlike find_user_restrictions, returns generator. Does not sort user restrictions.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[UserRestriction](toloka.client.user_restriction.UserRestriction.md), None, None\]

**Examples:**

```python
results_list = [restriction for restriction in toloka_client.get_user_restrictions(scope='ALL_PROJECTS')]
```
