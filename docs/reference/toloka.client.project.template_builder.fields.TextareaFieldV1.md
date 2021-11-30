# TextareaFieldV1
`toloka.client.project.template_builder.fields.TextareaFieldV1`

```
TextareaFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    disabled: Optional[Union[BaseComponent, bool]] = None,
    placeholder: Optional[Any] = None,
    resizable: Optional[Union[BaseComponent, bool]] = None,
    rows: Optional[Union[BaseComponent, float]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Box for entering multi-line text.


Use in tasks that require an extended response. For single-line responses, use the field.text component.

The size of the box does not automatically adjust to the length of the text. Users can change the height by
dragging the lower-right corner. To change the default size of the box, use the rows property.

Note that formatting is not available in the text box.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`disabled`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, editing is not available.</p>
`placeholder`|**Optional\[Any\]**|<p>A semi-transparent label that is shown when the box is empty. Use it to provide an example or a hint for the response.</p>
`resizable`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Changing the box size. When set to true (the default value), the user can change the height. To prevent resizing, set the value to false.</p>
`rows`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The height of the text box in lines.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
