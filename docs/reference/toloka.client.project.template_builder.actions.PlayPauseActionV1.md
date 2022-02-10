# PlayPauseActionV1
`toloka.client.project.template_builder.actions.PlayPauseActionV1`

```python
PlayPauseActionV1(
    self,
    view: Optional[Union[BaseComponent, RefComponent]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

This component controls audio or video playback. It stops playback in progress or starts if it is stopped.


For example, this component will allow you to play two videos simultaneously.

You can also stop or start playback for some event (plugin. trigger) or by pressing the hotkey (plugin.hotkeys).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`view`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [RefComponent](toloka.client.project.template_builder.base.RefComponent.md)\]\]**|<p>Points to the component that plays audio or video.</p>
