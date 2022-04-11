# AllConditionV1
`toloka.client.project.template_builder.conditions.AllConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/conditions.py#L45)

```python
AllConditionV1(
    self,
    conditions: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks that all child conditions are met.


If any of the conditions is not met, the component returns 'false'.

If you only need one out of several conditions to be met, use the condition.any component. You can also combine
these components.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`conditions`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>A set of conditions that must be met.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>

**Examples:**

How to check several conditions.

```python
coordinates_validation = tb.conditions.AllConditionV1(
    [
        tb.conditions.RequiredConditionV1(
            tb.data.OutputData('performer_coordinates'),
            hint="Couldn't get your coordinates. Please enable geolocation.",
        ),
        tb.conditions.DistanceConditionV1(
            tb.data.LocationData(),
            tb.data.InputData('coordinates'),
            500,
            hint='You are too far from the destination coordinates.',
        ),
    ],
)
```
