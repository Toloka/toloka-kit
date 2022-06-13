# UserRestrictionSearchRequest
`toloka.client.search_requests.UserRestrictionSearchRequest` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/search_requests.py#L741)

```python
UserRestrictionSearchRequest(
    self,
    scope: Optional[UserRestriction.Scope] = None,
    user_id: Optional[str] = None,
    project_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None
)
```

Parameters for searching user restriction

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scope`|**Optional\[[UserRestriction.Scope](toloka.client.user_restriction.UserRestriction.Scope.md)\]**|<p>The scope of the ban<ul><li>ALL_PROJECTS</li><li>PROJECT</li><li>POOL</li></ul></p>
`user_id`|**Optional\[str\]**|<p>Performer ID.</p>
`project_id`|**Optional\[str\]**|<p>The ID of the project that is blocked.</p>
`pool_id`|**Optional\[str\]**|<p>The ID of the pool that is blocked.</p>
`id_lt`|**Optional\[str\]**|<p>Bans with an ID less than the specified value.</p>
`id_lte`|**Optional\[str\]**|<p>Bans with an ID less than or equal to the specified value.</p>
`id_gt`|**Optional\[str\]**|<p>Bans with an ID greater than the specified value.</p>
`id_gte`|**Optional\[str\]**|<p>Bans with an ID greater than or equal to the specified value.</p>
`created_lt`|**Optional\[datetime\]**|<p>Bans created before the specified date.</p>
`created_lte`|**Optional\[datetime\]**|<p>Bans created before or on the specified date.</p>
`created_gt`|**Optional\[datetime\]**|<p>Bans created after the specified date.</p>
`created_gte`|**Optional\[datetime\]**|<p>Bans created after or on the specified date.</p>
