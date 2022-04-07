# RotateActionV1
`toloka.client.project.template_builder.actions.RotateActionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/actions.py#L128)

```python
RotateActionV1(
    self,
    view: Optional[Union[BaseComponent, RefComponent]] = None,
    payload: Optional[Union[BaseComponent, Payload]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Rotates the specified component by 90 degrees.


By default it rotates to the right, but you can specify the direction in the payload property.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`view`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [RefComponent](toloka.client.project.template_builder.base.RefComponent.md)\]\]**|<p>Points to the component to perform the action with.</p>
`payload`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Payload](toloka.client.project.template_builder.actions.RotateActionV1.Payload.md)\]\]**|<p>Sets the direction of rotation.</p>
