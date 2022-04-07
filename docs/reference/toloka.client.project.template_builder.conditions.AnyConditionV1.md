# AnyConditionV1
`toloka.client.project.template_builder.conditions.AnyConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/conditions.py#L79)

```python
AnyConditionV1(
    self,
    conditions: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks that at least one of the child conditions is met.


If none of the conditions is met, the component returns false.

If you need all conditions to be met, use the condition.all component. You can also combine these components.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`conditions`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>A set of conditions, at least one of which must be met.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
