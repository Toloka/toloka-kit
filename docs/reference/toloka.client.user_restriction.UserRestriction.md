# UserRestriction
`toloka.client.user_restriction.UserRestriction` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/user_restriction.py#L25)

```python
UserRestriction(
    self,
    *,
    user_id: Optional[str] = None,
    private_comment: Optional[str] = None,
    will_expire: Optional[datetime] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

Allows you to control the performer's access to your projects and pools


You can close user access to one or more projects. This allows you to control which users will perform tasks.
For example, you can select users with a skill value below N and block them from accessing tasks.
You can also unlock access.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Which performer is denied access.</p>
`private_comment`|**Optional\[str\]**|<p>A comment for you why access to this performer was restricted.</p>
`will_expire`|**Optional\[datetime\]**|<p>When access is restored. If you do not set the parameter, then the access restriction is permanent.</p>
`id`|**Optional\[str\]**|<p>The identifier of a specific fact of access restriction. Read only.</p>
`created`|**Optional\[datetime\]**|<p>Date and time when the fact of access restriction was created. Read only.</p>

**Examples:**

How you can lock access for one user on one project.

```python
new_restrict = toloka_client.set_user_restriction(
    ProjectUserRestriction(
        user_id='1',
        private_comment='I dont like you',
        project_id='5'
    )
)
```

And how you can unlock it.

```python
toloka_client.delete_user_restriction(new_restrict.id)
```
