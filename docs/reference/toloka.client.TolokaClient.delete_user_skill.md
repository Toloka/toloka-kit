# delete_user_skill
`toloka.client.TolokaClient.delete_user_skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
delete_user_skill(self, user_skill_id: str)
```

Drop specific UserSkill


UserSkill describe the skill value for a specific performer.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_skill_id`|**str**|<p>ID of the fact that the performer has a skill to delete.</p>

**Examples:**

```python
toloka_client.delete_user_skill(user_skill_id='1')
```
