# Restriction
`toloka.client.actions.Restriction`

```python
Restriction(
    self,
    *,
    scope: Union[UserRestriction.Scope, str, None] = None,
    duration_days: Optional[int] = None,
    private_comment: Optional[str] = None
)
```

Block access to projects or pools


It's better to use new version: RestrictionV2.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scope`|**Union\[[UserRestriction.Scope](toloka.client.user_restriction.UserRestriction.Scope.md), str, None\]**|<p><ul><li>POOL - Current pool where this rule was triggered. Does not affect the user&#x27;s rating.</li><li>PROJECT - Current project where this rule was triggered. Affects the user&#x27;s rating.</li><li>ALL_PROJECTS - All customer&#x27;s projects.</li></ul></p>
`duration_days`|**Optional\[int\]**|<p>Blocking period in days. By default, the lock is indefinite.</p>
`private_comment`|**Optional\[str\]**|<p>Comment (reason for blocking). Available only to the customer.</p>
