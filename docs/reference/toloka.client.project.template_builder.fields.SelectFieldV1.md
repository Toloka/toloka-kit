# SelectFieldV1
`toloka.client.project.template_builder.fields.SelectFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/fields.py#L451)

```python
SelectFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, Option]]]] = None,
    *,
    placeholder: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Button for selecting from a drop-down list.


Use this component when the list is long and only one option can be chosen.

For short lists (2-4 items), it's better to use field.radio-group or field.button-radio-group, where all the
options are visible at once.

To allow selecting multiple options, use the field.checkbox-group component.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`options`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Option](toloka.client.project.template_builder.fields.SelectFieldV1.Option.md)\]\]\]\]**|<p>Options to choose from.</p>
`placeholder`|**Optional\[Any\]**|<p>The text that will be displayed if none of the options is selected.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
