# UserRestrictionCursor
`toloka.streaming.cursor.UserRestrictionCursor`

```
UserRestrictionCursor(
    self,
    toloka_client: Union[TolokaClient, AsyncMultithreadWrapper[TolokaClient]],
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

Iterator over user restrictions by create time.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**Union\[[TolokaClient](toloka.client.TolokaClient.md), [AsyncMultithreadWrapper](toloka.util.async_utils.AsyncMultithreadWrapper.md)\[[TolokaClient](toloka.client.TolokaClient.md)\]\]**|<p>TolokaClient object that is being used to search user restrictions.</p>
`request`|**[UserRestrictionSearchRequest](toloka.client.search_requests.UserRestrictionSearchRequest.md)**|<p>Base request to search user restrictions.</p>

**Examples:**

Iterate over user restrictions in project.

```python
it = UserRestrictionCursor(toloka_client=toloka_client, project_id=my_proj_id)
current_restrictions = list(it)
new_restrictions = list(it)  # Contains only new user restrictions, appeared since the previous call.
```
