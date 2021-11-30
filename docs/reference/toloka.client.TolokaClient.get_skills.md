# get_skills
`toloka.client.TolokaClient.get_skills`

Finds all skills that match certain rules and returns them in an iterable object


Unlike find_skills, returns generator. Does not sort skills.
While iterating over the result, several requests to the Toloka server is possible.

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

* **Yields:**

  The next object corresponding to the request parameters.

* **Yield type:**

  Generator\[[Skill](toloka.client.skill.Skill.md), None, None\]

**Examples:**

How to check that a skill exists.

```python
segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
if segmentation_skill:
    print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
else:
    print('Create new segmentation skill here')
```
