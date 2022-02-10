# get_user_restriction
`toloka.client.TolokaClient.get_user_restriction`

```python
get_user_restriction(self, user_restriction_id: str)
```

Reads one specific user restriction

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_restriction_id`|**str**|<p>ID of the user restriction.</p>

* **Returns:**

  The user restriction.

* **Return type:**

  [UserRestriction](toloka.client.user_restriction.UserRestriction.md)

**Examples:**

```python
toloka_client.get_user_restriction(user_restriction_id='1')
```
