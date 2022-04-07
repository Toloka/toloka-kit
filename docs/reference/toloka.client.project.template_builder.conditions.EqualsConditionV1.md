# EqualsConditionV1
`toloka.client.project.template_builder.conditions.EqualsConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/conditions.py#L138)

```python
EqualsConditionV1(
    self,
    to: Optional[Any] = None,
    data: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks whether the original value is equal to the specified value.


If it matches, it returns true, otherwise it returns false.

When substituting values, you can refer to data.* or another element using $ref. You can also use helpers and
conditions to get the value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`to`|**Optional\[Any\]**|<p>The value to compare with the original. How to pass a value:<ul><li>Specify the value itself, like the number 42 or a string.</li><li>Get the value from your data.</li><li>Refer to another element using $ref.</li><li>Use helpers and conditions to get the value.</li></ul></p>
`data`|**Optional\[Any\]**|<p>Original value. If not specified, it uses the value returned by the parent component (the component that contains condition.equals). How to pass a value:     * Specify the value itself, like the number 42 or a string.     * Get the value from your data.     * Refer to another element using $ref.     * Use helpers and conditions to get the value.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
