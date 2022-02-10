# EmailFieldV1
`toloka.client.project.template_builder.fields.EmailFieldV1`

```python
EmailFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    placeholder: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Creates a field for entering an email address.


Checks that the text contains the @ character. You can set other conditions yourself.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`placeholder`|**Optional\[Any\]**|<p>A semi-transparent label that is shown in an empty field.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
