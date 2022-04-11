# NotConditionV1
`toloka.client.project.template_builder.conditions.NotConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/conditions.py#L181)

```python
NotConditionV1(
    self,
    condition: Optional[BaseComponent] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Returns the inverse of the specified condition.


For example, if the specified condition is met (returns true), then condition.not will return false.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`condition`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The condition for which the inverse is returned.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
