# EmptyConditionV1
`toloka.client.project.template_builder.conditions.EmptyConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/conditions.py#L122)

```python
EmptyConditionV1(
    self,
    data: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks that the data is empty (undefined).


Returns false if the data received a value.

You can check:
    Template data (data.*).
    Data for the input field (field.*) that contains condition.empty.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>Data to check. If not specified, data is checked in the component that contains condition.empty.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
