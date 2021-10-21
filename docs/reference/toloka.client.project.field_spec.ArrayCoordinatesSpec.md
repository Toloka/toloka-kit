# ArrayCoordinatesSpec
`toloka.client.project.field_spec.ArrayCoordinatesSpec`

```
ArrayCoordinatesSpec(
    self,
    *,
    required: Optional[bool] = True,
    hidden: Optional[bool] = False,
    current_location: Optional[bool] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None
)
```

Geographical coordinates array field specification

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`required`|**Optional\[bool\]**|<p>Whether the object or input field is required</p>
`hidden`|**Optional\[bool\]**|<p>Whether or not to hide the input value field from the user</p>
`current_location`|**Optional\[bool\]**|<p>put the user&#x27;s current coordinates in the field (true/false). Used in tasks for the mobile app.</p>
`min_size`|**Optional\[int\]**|<p>Minimum number of elements in the array</p>
`max_size`|**Optional\[int\]**|<p>Maximum number of elements in the array</p>
