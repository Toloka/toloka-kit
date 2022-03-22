# NotifyActionV1
`toloka.client.project.template_builder.actions.NotifyActionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/actions.py#L46)

```python
NotifyActionV1(
    self,
    payload: Optional[Union[BaseComponent, Payload]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

The component creates a message in the lower-left corner of the screen.


You can set the how long the message will be active, the delay before displaying it, and the background color.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`payload`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Payload](toloka.client.project.template_builder.actions.NotifyActionV1.Payload.md)\]\]**|<p>Parameters for the message.</p>
