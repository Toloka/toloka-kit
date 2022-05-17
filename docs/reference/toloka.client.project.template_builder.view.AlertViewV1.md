# AlertViewV1
`toloka.client.project.template_builder.view.AlertViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/view.py#L77)

```python
AlertViewV1(
    self,
    content: Optional[BaseComponent] = None,
    *,
    theme: Optional[Union[BaseComponent, Theme]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

The component creates a color block to highlight important information.


You can use both plain text and other visual components inside it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content of the block with important information.</p>
`theme`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Theme](toloka.client.project.template_builder.view.AlertViewV1.Theme.md)\]\]**|<p>Determines the block color.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
