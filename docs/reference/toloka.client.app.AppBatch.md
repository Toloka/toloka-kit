# AppBatch
`toloka.client.app.AppBatch`

```
AppBatch(
    self,
    *,
    id: Optional[str] = None,
    app_project_id: Optional[str] = None,
    name: Optional[str] = None,
    status: Union[Status, str, None] = None,
    items_count: Optional[int] = None,
    item_price: Optional[Decimal] = None,
    cost: Optional[Decimal] = None,
    created_at: Optional[datetime] = None,
    started_at: Optional[datetime] = None,
    finished_at: Optional[datetime] = None
)
```

A batch of data that you send for labeling at a time. The batch consists of work items.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Batch ID.</p>
`app_project_id`|**Optional\[str\]**|<p>Project ID.</p>
`name`|**Optional\[str\]**|<p></p>
`status`|**Optional\[[Status](toloka.client.app.AppBatch.Status.md)\]**|<p>The state of the batch, calculated based on the states of items comprising it. Allowed values:<ul><li>NEW</li><li>PROCESSING</li><li>COMPLETED</li><li>ERROR</li><li>CANCELLED</li><li>ARCHIVE</li><li>NO_MONEY</li></ul></p>
`items_count`|**Optional\[int\]**|<p>Number of items in the batch.</p>
`item_price`|**Optional\[Decimal\]**|<p>The cost of processing per item in a batch.</p>
`cost`|**Optional\[Decimal\]**|<p>The cost of processing per batch.</p>
`created_at`|**Optional\[datetime\]**|<p>Date and time when the batch was created.</p>
`started_at`|**Optional\[datetime\]**|<p>Date and time when batch processing started.</p>
`finished_at`|**Optional\[datetime\]**|<p>Date and time when batch processing was completed.</p>
