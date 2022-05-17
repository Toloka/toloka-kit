# LocalData
`toloka.client.project.template_builder.data.LocalData` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/data.py#L63)

```python
LocalData(
    self,
    path: Optional[Any] = None,
    default: Optional[Any] = None
)
```

The local data available only from inside the component.


This data is used in some auxiliary components, such as helper.transform.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`path`|**Optional\[Any\]**|<p>Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the path to the array element, specify its sequence number starting from zero, for example: items.0</p>
`default`|**Optional\[Any\]**|<p>The value to be used as the default data. This value will be shown in the interface, so it might hide some placeholders, for example, in the field.text component.</p>
