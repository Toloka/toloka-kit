# get_user_skills
`toloka.client.TolokaClient.get_user_skills`

Finds all user skills that match certain rules and returns them in an iterable object


UserSkill describe the skill value for a specific performer.
Unlike find_user_skills, returns generator. Does not sort user skills.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[UserSkill](toloka.client.user_skill.UserSkill.md), None, None\]

**Examples:**

```python
results_list = [skill for skill in toloka_client.get_user_skills()]
```
