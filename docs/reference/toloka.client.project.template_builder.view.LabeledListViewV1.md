# LabeledListViewV1
`toloka.client.project.template_builder.view.LabeledListViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/view.py#L247)

```python
LabeledListViewV1(
    self,
    items: Optional[Union[BaseComponent, List[Union[BaseComponent, Item]]]] = None,
    *,
    min_width: Optional[Union[BaseComponent, float]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Displaying components as a list with labels placed on the left.


If you don't need labels, use view.list.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Item](toloka.client.project.template_builder.view.LabeledListViewV1.Item.md)\]\]\]\]**|<p>List items.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The minimum width of list content. If the component width is less than the specified value, it switches to compact mode.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
