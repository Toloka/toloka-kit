# set_user_skill
`toloka.client.TolokaClient.set_user_skill`

Sets the skill value to the performer

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`skill_id`|**Optional\[str\]**|<p>Skill ID. What skill to set.</p>
`user_id`|**Optional\[str\]**|<p>User ID. Which user.</p>
`value`|**Optional\[Decimal\]**|<p>Fractional value of the skill. Minimum - 0, maximum - 100.</p>

* **Returns:**

  Сreated fact of skill installation.

* **Return type:**

  [UserSkill](toloka.client.user_skill.UserSkill.md)

**Examples:**

```python
from decimal import *
toloka_client.set_user_skill(skill_id='1', user_id='1', value=Decimal(100))
```
