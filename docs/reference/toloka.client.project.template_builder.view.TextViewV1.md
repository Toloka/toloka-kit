# TextViewV1
`toloka.client.project.template_builder.view.TextViewV1`

```python
TextViewV1(
    self,
    content: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Block for displaying text.


If you need formatted text, use view.markdown.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[Any\]**|<p>The text displayed in the block. To insert a new line, use </p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>

**Examples:**

How to show labeled field from the task inputs.

```python
text_view = tb.view.TextViewV1(tb.data.InputData('input_field_name'), label='My label:')
```
