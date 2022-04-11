# ColumnsLayoutV1
`toloka.client.project.template_builder.layouts.ColumnsLayoutV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/layouts.py#L58)

```python
ColumnsLayoutV1(
    self,
    items: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    *,
    full_height: Optional[Union[BaseComponent, bool]] = None,
    min_width: Optional[Union[BaseComponent, float]] = None,
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = None,
    vertical_align: Optional[Union[BaseComponent, VerticalAlign]] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component for placing content in columns.


Use it to customize the display of content: set the column width and adjust the vertical alignment of content.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>Columns to divide the interface into.</p>
`full_height`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Switches the component to column mode at full height and with individual scrolling. Otherwise, the height is determined by the height of the column that is filled in the most.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The minimum width of the component; if it is narrower, columns are output sequentially, one by one.</p>
`ratio`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]\]\]**|<p>An array of values that specify the relative width of columns. For example, if you have 3 columns, the value [1,2,1] divides the space into 4 parts and the column in the middle is twice as large as the other columns. If the number of columns exceeds the number of values in the ratio property, the values are repeated. For example, if you have 4 columns and the ratio is set to [1,2], the result is the same as for [1,2,1,2]. If the number of columns is less than the number of values in the ratio property, extra values are simply ignored.</p>
`vertical_align`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [VerticalAlign](toloka.client.project.template_builder.layouts.ColumnsLayoutV1.VerticalAlign.md)\]\]**|<p>Vertical alignment of column content.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
