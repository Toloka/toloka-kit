# ArrayStringSpec
`toloka.client.project.field_spec.ArrayStringSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/field_spec.py#L153)

```python
ArrayStringSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allowed_values: Optional[List[str]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None
)
```

A string array field specification

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`min_length`|**Optional\[int\]**|<p>Minimum length of the string</p>
`max_length`|**Optional\[int\]**|<p>Maximum length of the string</p>
`allowed_values`|**Optional\[List\[str\]\]**|<p>Allowed values</p>
`min_size`|**Optional\[int\]**|<p>Minimum number of elements in the array</p>
`max_size`|**Optional\[int\]**|<p>Maximum number of elements in the array</p>
