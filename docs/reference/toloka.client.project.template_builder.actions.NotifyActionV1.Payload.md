# Payload
`toloka.client.project.template_builder.actions.NotifyActionV1.Payload`

```
Payload(
    self,
    content: Optional[Any] = None,
    theme: Optional[Union[BaseComponent, Theme]] = None,
    *,
    delay: Optional[Union[BaseComponent, float]] = None,
    duration: Optional[Union[BaseComponent, float]] = None
)
```

Parameters for the message.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[Any\]**|<p>Message text</p>
`theme`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Theme](toloka.client.project.template_builder.actions.NotifyActionV1.Payload.Theme.md)\]\]**|<p>The background color of the message.</p>
`delay`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The duration of the delay (in milliseconds) before the message appears.</p>
`duration`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The duration of the message activity (in milliseconds), which includes the duration of the delay before displaying it. For example, if duration is 1000 and delay is 400, the message will be displayed for 600 milliseconds.</p>
