# ArrayBooleanSpec
`toloka.client.project.field_spec.ArrayBooleanSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/field_spec.py#L141)

```python
ArrayBooleanSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    allowed_values: Optional[List[bool]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None
)
```

A boolean array field specification

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`allowed_values`|**Optional\[List\[bool\]\]**|<p>Allowed values</p>
`min_size`|**Optional\[int\]**|<p>Minimum number of elements in the array</p>
`max_size`|**Optional\[int\]**|<p>Maximum number of elements in the array</p>
