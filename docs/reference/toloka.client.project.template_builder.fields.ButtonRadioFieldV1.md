# ButtonRadioFieldV1
`toloka.client.project.template_builder.fields.ButtonRadioFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/fields.py#L87)

```python
ButtonRadioFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    value_to_set: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component in the form of a button.


The user makes a choice by clicking on it.

The size of the button depends on the size of the label.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`value_to_set`|**Optional\[Any\]**|<p>The value of the output data when the button is clicked.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
