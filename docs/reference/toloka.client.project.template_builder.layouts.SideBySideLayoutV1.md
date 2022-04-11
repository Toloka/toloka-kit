# SideBySideLayoutV1
`toloka.client.project.template_builder.layouts.SideBySideLayoutV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/layouts.py#L141)

```python
SideBySideLayoutV1(
    self,
    controls: Optional[BaseComponent] = None,
    items: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    *,
    min_item_width: Optional[Union[BaseComponent, float]] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

The component displays several data blocks of the same width on a single horizontal panel.


For example, you can use this to compare several photos.

You can set the minimum width for data blocks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`controls`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Components that let users perform the required actions. For example: field.checkbox-group or field.button-radio-group.</p>
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>An array of data blocks.</p>
`min_item_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The minimum width of a data block, at least 400 pixels.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
