# StringSpec
`toloka.client.project.field_spec.StringSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/field_spec.py#L72)

```python
StringSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    allowed_values: Optional[List[str]] = None
)
```

A string field specification

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`min_length`|**Optional\[int\]**|<p>Minimum length of the string</p>
`max_length`|**Optional\[int\]**|<p>Maximum length of the string</p>
`allowed_values`|**Optional\[List\[str\]\]**|<p>Allowed values</p>
