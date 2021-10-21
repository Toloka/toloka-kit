# set_user_restriction
`toloka.client.TolokaClient.set_user_restriction`

```
set_user_restriction(self, user_restriction: UserRestriction)
```

Closes the performer's access to one or more projects

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_restriction`|**[UserRestriction](toloka.client.user_restriction.UserRestriction.md)**|<p>To whom and what to prohibit.</p>

* **Returns:**

  Created restriction object.

* **Return type:**

  [UserRestriction](toloka.client.user_restriction.UserRestriction.md)

**Examples:**

If performer often makes mistakes, we will restrict access to all our projects.

```python
new_restriction = toloka_client.set_user_restriction(
    toloka.user_restriction.ProjectUserRestriction(
        user_id='1',
        private_comment='Performer often makes mistakes',
        project_id='5'
    )
)
```
