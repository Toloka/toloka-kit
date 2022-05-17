# get_user_bonus
`toloka.client.TolokaClient.get_user_bonus` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
get_user_bonus(self, user_bonus_id: str)
```

Reads one specific user bonus

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_bonus_id`|**str**|<p>ID of the user bonus.</p>

* **Returns:**

  The user bonus.

* **Return type:**

  [UserBonus](toloka.client.user_bonus.UserBonus.md)

**Examples:**

```python
toloka_client.get_user_bonus(user_bonus_id='1')
```
