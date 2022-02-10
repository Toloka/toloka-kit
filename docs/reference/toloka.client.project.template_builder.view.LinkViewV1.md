# LinkViewV1
`toloka.client.project.template_builder.view.LinkViewV1`

```python
LinkViewV1(
    self,
    url: Optional[Any] = None,
    *,
    content: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Universal way to add a link.


This link changes color when clicked.

We recommend using this component if you need to insert a link without additional formatting.

If you want to insert a button that will open the link, use the view.action-button and action.open-link components.

To insert a link with a search query, use helper.search-query.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`url`|**Optional\[Any\]**|<p>Link URL.</p>
`content`|**Optional\[Any\]**|<p>Link text displayed to the user.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
