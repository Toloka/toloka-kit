# DateFieldV1
`toloka.client.project.template_builder.fields.DateFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/fields.py#L174)

```python
DateFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    format: Optional[Any] = None,
    *,
    block_list: Optional[Union[BaseComponent, List[Any]]] = None,
    max: Optional[Any] = None,
    min: Optional[Any] = None,
    placeholder: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component for entering the date and time in the desired format and range.


You can set a list of dates that the user cannot select.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`format`|**Optional\[Any\]**|<p>Format of the date entered by the user:<ul><li>date-time — date and time.</li><li>date — date only.</li></ul></p>
`block_list`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Any\]\]\]**|<p>List of dates that the user cannot select.<ul><li>block_list[]: Date that the user cannot select.</li></ul></p>
`max`|**Optional\[Any\]**|<p>The latest date and time in the YYYY-MM-DD hh:mm format that the user can select. Where:<ul><li>YYYY is the year.</li><li>MM is the month.</li><li>DD is the day.</li><li>hh is the time in hours.</li><li>mm is the time in minutes.</li></ul></p>
`min`|**Optional\[Any\]**|<p>The earliest date and time in the YYYY-MM-DD hh:mm format that the user can select. Where:<ul><li>YYYY is the year.</li><li>MM is the month.</li><li>DD is the day.</li><li>hh is the time in hours.</li><li>mm is the time in minutes.</li></ul></p>
`placeholder`|**Optional\[Any\]**|<p>A semi-transparent label that is shown in the box when it is empty.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
