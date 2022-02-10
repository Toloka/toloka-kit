# PhoneNumberFieldV1
`toloka.client.project.template_builder.fields.PhoneNumberFieldV1`

```python
PhoneNumberFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    placeholder: Optional[Union[BaseComponent, str]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Creates a field for entering a phone number.


Allows entering numbers, spaces, and the +, ( ), - characters. Only numbers and the + character at the beginning
will remain in the data. For example, if you enter +7 (012) 345-67-89, the data gets the +70123456789 value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`placeholder`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>A semi-transparent label that is shown in an empty field.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
