# TextAnnotationHotkeysPluginV1
`toloka.client.project.template_builder.plugins.TextAnnotationHotkeysPluginV1`

```
TextAnnotationHotkeysPluginV1(
    self,
    labels: Optional[Union[BaseComponent, List[str]]] = None,
    remove: Optional[Union[BaseComponent, str]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Use this to set keyboard shortcuts for the field.text-annotation component.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`labels`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[str\]\]\]**|<p>Keyboard shortcuts for selecting categories. They&#x27;re assigned to buttons with categories in the order they&#x27;re shown.</p>
`remove`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Use this property to allow the performer to deselect an entire line or part of it. The key that you assign to this property will deselect.</p>
