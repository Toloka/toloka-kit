# CoordinatesSpec
`toloka.client.project.field_spec.CoordinatesSpec` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/field_spec.py#L124)

```python
CoordinatesSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    current_location: Optional[bool] = None
)
```

Geographical coordinates field specification, such as “53.910236,27.531110

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`current_location`|**Optional\[bool\]**|<p>put the user&#x27;s current coordinates in the field (true/false). Used in tasks for the mobile app.</p>
