# AppItem
`toloka.client.app.AppItem` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/app/__init__.py#L100)

```python
AppItem(
    self,
    *,
    batch_id: Optional[str] = None,
    input_data: Optional[Dict[str, Any]] = None,
    id: Optional[str] = None,
    app_project_id: Optional[str] = None,
    created: Optional[datetime] = None,
    updated: Optional[datetime] = None,
    status: Union[Status, str, None] = None,
    output_data: Optional[Dict[str, Any]] = None,
    errors: Optional[List[_AppError]] = None,
    created_at: Optional[datetime] = None,
    started_at: Optional[datetime] = None,
    finished_at: Optional[datetime] = None
)
```

A work item with data. It's uploaded into the batch with other items to be collectively sent for labeling.


In a TSV file with tasks, each line is a work item.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`batch_id`|**Optional\[str\]**|<p>ID of the batch that includes the item.</p>
`input_data`|**Optional\[Dict\[str, Any\]\]**|<p>The item data following the App schema.</p>
`id`|**Optional\[str\]**|<p>Item ID.</p>
`app_project_id`|**Optional\[str\]**|<p>ID of the app project that includes the batch with this item.</p>
`created`|**Optional\[datetime\]**|<p></p>
`updated`|**Optional\[datetime\]**|<p></p>
`status`|**Optional\[[Status](toloka.client.app.AppItem.Status.md)\]**|<p>Processing status. If the item has the NEW status, it can be edited. In other statuses, the item is immutable. Allowed values:<ul><li>NEW - new;</li><li>PROCESSING - being processed;</li><li>COMPLETED - processing complete;</li><li>ERROR - error during processing;</li><li>CANCELLED - processing canceled;</li><li>ARCHIVE - item has been archived;</li><li>NO_MONEY - not enough money for processing.</li></ul></p>
`output_data`|**Optional\[Dict\[str, Any\]\]**|<p>Processing result.</p>
`errors`|**Optional\[List\[[_AppError](toloka.client.app._AppError.md)\]\]**|<p></p>
`created_at`|**Optional\[datetime\]**|<p>Date and time when the item was created.</p>
`started_at`|**Optional\[datetime\]**|<p>Date and time when the item processing started.</p>
`finished_at`|**Optional\[datetime\]**|<p>Date and time when the item processing was completed.</p>
