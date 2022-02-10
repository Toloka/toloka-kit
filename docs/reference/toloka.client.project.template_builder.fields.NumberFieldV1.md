# NumberFieldV1
`toloka.client.project.template_builder.fields.NumberFieldV1`

```python
NumberFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    maximum: Optional[Union[BaseComponent, int]] = None,
    minimum: Optional[Union[BaseComponent, int]] = None,
    placeholder: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component that allows you to enter a number.


The box already has validation: by default, users can enter only numbers and decimal separators. They can use either
a dot or a comma as a separator, but there will always be a dot in the output.

When the user is entering a number, the separator automatically changes to the one specified in the regional
settings. For Russia, the separator is a comma.

Negative numbers are allowed by default. To disable them, use the validation property. Pressing the up or down arrow
keys will increase or decrease the number by one.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`maximum`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), int\]\]**|<p>Maximum number that can be entered.</p>
`minimum`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), int\]\]**|<p>Minimum number that can be entered.</p>
`placeholder`|**Optional\[Any\]**|<p>A semi-transparent label that is shown in the box when it is empty.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
