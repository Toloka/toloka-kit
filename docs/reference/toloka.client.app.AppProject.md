# AppProject
`toloka.client.app.AppProject` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/app/__init__.py#L31)

```python
AppProject(
    self,
    *,
    app_id: Optional[str] = None,
    parent_app_project_id: Optional[str] = None,
    name: Optional[str] = None,
    parameters: Optional[Dict] = None,
    id: Optional[str] = None,
    status: Union[Status, str, None] = None,
    created: Optional[datetime] = None,
    item_price: Optional[Decimal] = None,
    errors: Optional[List[_AppError]] = None
)
```

An App project with the parameters that you specify when creating it. It will have the interface and quality


control already pre-configured, decomposition done, and everything ready to use: all you need is to upload batches
and send them for labeling.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`app_id`|**Optional\[str\]**|<p></p>
`parent_app_project_id`|**Optional\[str\]**|<p></p>
`name`|**Optional\[str\]**|<p></p>
`parameters`|**Optional\[Dict\]**|<p></p>
`id`|**Optional\[str\]**|<p></p>
`status`|**Optional\[[Status](toloka.client.app.AppProject.Status.md)\]**|<p>Project statuses for asynchronous creation. Allowed values:<ul><li>CREATING</li><li>READY</li><li>ARCHIVE</li><li>ERROR</li></ul></p>
`created`|**Optional\[datetime\]**|<p></p>
`item_price`|**Optional\[Decimal\]**|<p></p>
`errors`|**Optional\[List\[[_AppError](toloka.client.app._AppError.md)\]\]**|<p></p>
