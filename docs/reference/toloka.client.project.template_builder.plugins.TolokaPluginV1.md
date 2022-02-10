# TolokaPluginV1
`toloka.client.project.template_builder.plugins.TolokaPluginV1`

```python
TolokaPluginV1(
    self,
    kind: Optional[TolokaPluginLayout.Kind] = None,
    *,
    task_width: Optional[float] = None,
    notifications: Optional[Union[BaseComponent, List[BaseComponent]]] = None,
    version: Optional[str] = '1.0.0'
)
```

A plugin with extra settings for tasks in Toloka.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`layout`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [TolokaPluginLayout](toloka.client.project.template_builder.plugins.TolokaPluginV1.TolokaPluginLayout.md)\]\]**|<p>Settings for the task appearance in Toloka.</p>
`notifications`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]\]\]**|<p>Notifications shown at the top of the page.</p>

**Examples:**

How to set the task width on the task page.

```python
task_width_plugin = tb.plugins.TolokaPluginV1(
    'scroll',
    task_width=400,
)
```
