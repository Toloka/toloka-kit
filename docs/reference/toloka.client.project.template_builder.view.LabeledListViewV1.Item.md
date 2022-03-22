# Item
`toloka.client.project.template_builder.view.LabeledListViewV1.Item` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/view.py#L257)

```python
Item(
    self,
    content: Optional[BaseComponent] = None,
    label: Optional[Any] = None,
    *,
    center_label: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None
)
```

Item.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>List item content.</p>
`label`|**Optional\[Any\]**|<p>A label displayed next to a list item.</p>
`center_label`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, a label is center-aligned relative to the content of a list item (content). Use it if the list consists of large items, such as images or multi-line text. By default, false (the label is aligned to the top of the content block).</p>
`hint`|**Optional\[Any\]**|<p>A pop-up hint displayed next to a label.</p>
