# AssignmentCursor
`toloka.streaming.cursor.AssignmentCursor`

```python
AssignmentCursor(
    self,
    toloka_client: Union[TolokaClient, AsyncMultithreadWrapper[TolokaClient]],
    event_type: Any,
    status: Union[str, Assignment.Status, List[Union[str, Assignment.Status]]] = None,
    task_id: Optional[str] = None,
    task_suite_id: Optional[str] = None,
    pool_id: Optional[str] = None,
    user_id: Optional[str] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    submitted_lt: Optional[datetime] = None,
    submitted_lte: Optional[datetime] = None,
    submitted_gt: Optional[datetime] = None,
    submitted_gte: Optional[datetime] = None,
    accepted_lt: Optional[datetime] = None,
    accepted_lte: Optional[datetime] = None,
    accepted_gt: Optional[datetime] = None,
    accepted_gte: Optional[datetime] = None,
    rejected_lt: Optional[datetime] = None,
    rejected_lte: Optional[datetime] = None,
    rejected_gt: Optional[datetime] = None,
    rejected_gte: Optional[datetime] = None,
    skipped_lt: Optional[datetime] = None,
    skipped_lte: Optional[datetime] = None,
    skipped_gt: Optional[datetime] = None,
    skipped_gte: Optional[datetime] = None,
    expired_lt: Optional[datetime] = None,
    expired_lte: Optional[datetime] = None,
    expired_gt: Optional[datetime] = None,
    expired_gte: Optional[datetime] = None
)
```

Iterator over Assignment objects of seleted AssignmentEventType.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**Union\[[TolokaClient](toloka.client.TolokaClient.md), [AsyncMultithreadWrapper](toloka.util.async_utils.AsyncMultithreadWrapper.md)\[[TolokaClient](toloka.client.TolokaClient.md)\]\]**|<p>TolokaClient object that is being used to search assignments.</p>
`request`|**[AssignmentSearchRequest](toloka.client.search_requests.AssignmentSearchRequest.md)**|<p>Base request to search assignments by.</p>
`event_type`|**Any**|<p>Assignments event&#x27;s type to search.</p>

**Examples:**

Iterate over assignment acceptances events.

```python
it = AssignmentCursor(pool_id='123', event_type='ACCEPTED', toloka_client=toloka_client)
current_events = list(it)
new_events = list(it)  # Contains only new events, occured since the previous call.
```
