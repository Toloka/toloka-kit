# get_skill
`toloka.client.TolokaClient.get_skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
get_skill(self, skill_id: str)
```

Reads one specific skill

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`skill_id`|**str**|<p>ID of the skill.</p>

* **Returns:**

  The skill.

* **Return type:**

  [Skill](toloka.client.skill.Skill.md)

**Examples:**

```python
toloka_client.get_skill(skill_id='1')
```
