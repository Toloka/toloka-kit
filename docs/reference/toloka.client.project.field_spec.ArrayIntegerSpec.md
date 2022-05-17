# ArrayIntegerSpec
`toloka.client.project.field_spec.ArrayIntegerSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/field_spec.py#L165)

```python
ArrayIntegerSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
    allowed_values: Optional[List[int]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None
)
```

An integer array field specification

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`min_value`|**Optional\[int\]**|<p>Minimum value of the number</p>
`max_value`|**Optional\[int\]**|<p>Maximum value of the number</p>
`allowed_values`|**Optional\[List\[int\]\]**|<p>Allowed values</p>
`min_size`|**Optional\[int\]**|<p>Minimum number of elements in the array</p>
`max_size`|**Optional\[int\]**|<p>Maximum number of elements in the array</p>
