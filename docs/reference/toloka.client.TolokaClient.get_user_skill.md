# get_user_skill
`toloka.client.TolokaClient.get_user_skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/__init__.py#L40)

```python
get_user_skill(self, user_skill_id: str)
```

Gets the value of the user's skill


UserSkill describe the skill value for a specific performer.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_skill_id`|**str**|<p>ID of the user skill.</p>

* **Returns:**

  The skill value.

* **Return type:**

  [UserSkill](toloka.client.user_skill.UserSkill.md)

**Examples:**

```python
toloka_client.get_user_skill(user_skill_id='1')
```
