# find_user_bonuses
`toloka.client.TolokaClient.find_user_bonuses`

Finds all user bonuses that match certain rules


As a result, it returns an object that contains the first part of the found user bonuses and whether there
are any more results.
It is better to use the "get_user_bonuses" method, they allow to iterate trought all results
and not just the first output.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`assignment_id`|**Optional\[str\]**|<p>ID of the performer&#x27;s response to the task a reward is issued for.</p>
`private_comment`|**Optional\[str\]**|<p>Comments for the requester.</p>
`id_lt`|**Optional\[str\]**|<p>Bonuses with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Bonuses with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Bonuses with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Bonuses with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Bonuses awarded before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Bonuses awarded before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Bonuses awarded after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Bonuses awarded after or on the specified date.</p>
`sort`|**Union\[List\[str\], [UserBonusSortItems](toloka.client.search_requests.UserBonusSortItems.md), None\]**|<p>How to sort result. Defaults to None.</p>
`limit`|**Optional\[int\]**|<p>Limit on the number of results returned.</p>

* **Returns:**

  The first `limit` user bonuses in `items`.
And a mark that there is more.

* **Return type:**

  [UserBonusSearchResult](toloka.client.search_results.UserBonusSearchResult.md)

**Examples:**

```python
toloka_client.find_user_bonuses(user_id='1', sort=['-created', '-id'], limit=3)
```

If method finds more objects than custom or system `limit` allows to operate, it will also show an indicator `has_more=True`.
