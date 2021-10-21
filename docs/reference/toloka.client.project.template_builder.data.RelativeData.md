# RelativeData
`toloka.client.project.template_builder.data.RelativeData`

```
RelativeData(
    self,
    path: Optional[Any] = None,
    default: Optional[Any] = None
)
```

A special component for saving data.


It's only available in the field.list component.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`path`|**Optional\[Any\]**|<p>Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the path to the array element, specify its sequence number starting from zero, for example: items.0</p>
`default`|**Optional\[Any\]**|<p>The value to be used as the default data. This value will be shown in the interface, so it might hide some placeholders, for example, in the field.text component.</p>
