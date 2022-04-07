# UserSkillCursor
`toloka.streaming.cursor.UserSkillCursor` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/cursor.py#L330)

```python
UserSkillCursor(
    self,
    toloka_client: Union[TolokaClient, AsyncMultithreadWrapper[TolokaClient]],
    event_type: Any,
    user_id: Optional[str] = None,
    skill_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    modified_lt: Optional[datetime] = None,
    modified_lte: Optional[datetime] = None,
    modified_gt: Optional[datetime] = None,
    modified_gte: Optional[datetime] = None
)
```

Iterator over UserSkillEvent objects of seleted event_type.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**Union\[[TolokaClient](toloka.client.TolokaClient.md), [AsyncMultithreadWrapper](toloka.util.async_utils.AsyncMultithreadWrapper.md)\[[TolokaClient](toloka.client.TolokaClient.md)\]\]**|<p>TolokaClient object that is being used to search user skills.</p>
`request`|**[UserSkillSearchRequest](toloka.client.search_requests.UserSkillSearchRequest.md)**|<p>Base request to search user skills by.</p>
`event_type`|**Any**|<p>User skill event&#x27;s type to search.</p>

**Examples:**

Iterate over user skills acceptances events.

```python
it = UserSkillCursor(event_type='MODIFIED', toloka_client=toloka_client)
current_events = list(it)
new_events = list(it)  # Contains only new events, occured since the previous call.
```
