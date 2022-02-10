# delete_user_restriction
`toloka.client.TolokaClient.delete_user_restriction`

```python
delete_user_restriction(self, user_restriction_id: str)
```

Unlocks existing restriction

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_restriction_id`|**str**|<p>Restriction that should be removed.</p>

**Examples:**

```python
toloka_client.delete_user_restriction(user_restriction_id='1')
```
