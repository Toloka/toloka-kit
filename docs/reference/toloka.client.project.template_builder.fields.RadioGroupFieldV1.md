# RadioGroupFieldV1
`toloka.client.project.template_builder.fields.RadioGroupFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/fields.py#L421)

```python
RadioGroupFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = None,
    *,
    disabled: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component for selecting one value out of several options. It is designed as a group of circles arranged vertically.


If you want it to look like normal buttons, use field.button-radio-group.

The minimum number of buttons is one. Any type of data can be returned.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`options`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [GroupFieldOption](toloka.client.project.template_builder.fields.GroupFieldOption.md)\]\]\]\]**|<p>List of options to choose from</p>
`disabled`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>This property prevents clicking the button. If the value is true, the button is not active (the user will not be able to click it).</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>

**Examples:**

How to add label selector to interface.

```python
radio_group_field = tb.fields.RadioGroupFieldV1(
    tb.data.OutputData(path='result'),
    [
        tb.fields.GroupFieldOption('Cat', 'cat'),
        tb.fields.GroupFieldOption('Dog', 'dog'),
    ],
    validation=tb.conditions.RequiredConditionV1()
)
```
