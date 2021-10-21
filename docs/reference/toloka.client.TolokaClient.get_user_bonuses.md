# get_user_bonuses
`toloka.client.TolokaClient.get_user_bonuses`

Finds all user bonuses that match certain rules and returns them in an iterable object


Unlike find_user_bonuses, returns generator. Does not sort user bonuses.
While iterating over the result, several requests to the Toloka server is possible.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`private_comment`|**Optional\[str\]**|<p>Comments for the requester.</p>
`id_lt`|**Optional\[str\]**|<p>Bonuses with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Bonuses with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Bonuses with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Bonuses with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Bonuses awarded before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Bonuses awarded before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Bonuses awarded after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Bonuses awarded after or on the specified date.</p>

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[UserBonus](toloka.client.user_bonus.UserBonus.md), None, None\]

**Examples:**

```python
bonuses = [bonus for bonus in toloka_client.get_user_bonuses(created_lt='2021-06-01T00:00:00')]
```
