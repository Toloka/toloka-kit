# UserBonusCursor
`toloka.streaming.cursor.UserBonusCursor`

```
UserBonusCursor(
    self,
    toloka_client: Union[TolokaClient, ...],
    user_id: Optional[str] = None,
    private_comment: Optional[str] = None,
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

Iterator over user bonuses by create time.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**Union\[[TolokaClient](toloka.client.TolokaClient.md), ...\]**|<p>TolokaClient object that is being used to search user bonuses.</p>
`request`|**[UserBonusSearchRequest](toloka.client.search_requests.UserBonusSearchRequest.md)**|<p>Base request to search user bonuses by.</p>

**Examples:**

Iterate over user bonuses.

```python
it = UserBonusCursor(toloka_client=toloka_client)
current_bonuses = list(it)
new_bonuses = list(it)  # Contains only new user bonuses, appeared since the previous call.
```
