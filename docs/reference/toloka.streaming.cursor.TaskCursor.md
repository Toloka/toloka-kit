# TaskCursor
`toloka.streaming.cursor.TaskCursor`

```
TaskCursor(
    self,
    toloka_client: Union[TolokaClient, ...],
    pool_id: Optional[str] = None,
    overlap: Optional[int] = None,
    id_lt: Optional[str] = None,
    id_lte: Optional[str] = None,
    id_gt: Optional[str] = None,
    id_gte: Optional[str] = None,
    created_lt: Optional[datetime] = None,
    created_lte: Optional[datetime] = None,
    created_gt: Optional[datetime] = None,
    created_gte: Optional[datetime] = None,
    overlap_lt: Optional[int] = None,
    overlap_lte: Optional[int] = None,
    overlap_gt: Optional[int] = None,
    overlap_gte: Optional[int] = None
)
```

Iterator over tasks by create time.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**Union\[[TolokaClient](toloka.client.TolokaClient.md), ...\]**|<p>TolokaClient object that is being used to search tasks.</p>
`request`|**[TaskSearchRequest](toloka.client.search_requests.TaskSearchRequest.md)**|<p>Base request to search tasks by.</p>

**Examples:**

Iterate over tasks.

```python
it = TaskCursor(pool_id='123', toloka_client=toloka_client)
current_tasks = list(it)
new_tasks = list(it)  # Contains only new tasks, appeared since the previous call.
```
