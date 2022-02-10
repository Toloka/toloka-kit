# FieldSpec
`toloka.client.project.field_spec.FieldSpec`

```python
FieldSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False
)
```

A base class for field specifications used in project's `input_spec` and `output_spec`


for input and respose data validation specification respectively. Use subclasses of this
class defined below to define the data type (string, integer, URL, etc.) and specify
validation parameters (such as string length).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
