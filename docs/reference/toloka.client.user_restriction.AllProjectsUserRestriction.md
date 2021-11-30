# AllProjectsUserRestriction
`toloka.client.user_restriction.AllProjectsUserRestriction`

```
AllProjectsUserRestriction(
    self,
    *,
    user_id: Optional[str] = None,
    private_comment: Optional[str] = None,
    will_expire: Optional[datetime] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

Forbid the performer from doing tasks from all your projects

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Which performer is denied access.</p>
`private_comment`|**Optional\[str\]**|<p>A comment for you why access to this performer was restricted.</p>
`will_expire`|**Optional\[datetime\]**|<p>When access is restored. If you do not set the parameter, then the access restriction is permanent.</p>
`id`|**Optional\[str\]**|<p>The identifier of a specific fact of access restriction. Read only.</p>
`created`|**Optional\[datetime\]**|<p>Date and time when the fact of access restriction was created. Read only.</p>
