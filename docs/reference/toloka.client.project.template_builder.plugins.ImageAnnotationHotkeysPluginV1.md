# ImageAnnotationHotkeysPluginV1
`toloka.client.project.template_builder.plugins.ImageAnnotationHotkeysPluginV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/plugins.py#L26)

```python
ImageAnnotationHotkeysPluginV1(
    self,
    *,
    cancel: Optional[Union[BaseComponent, str]] = None,
    confirm: Optional[Union[BaseComponent, str]] = None,
    labels: Optional[Union[BaseComponent, List[str]]] = None,
    point: Optional[str] = None,
    polygon: Optional[str] = None,
    rectangle: Optional[str] = None,
    select: Optional[str] = None,
    version: Optional[str] = '1.0.0'
)
```

Used to set hotkeys for the field.image-annotation component.


You can set hotkeys to select area types and selection modes and to confirm or cancel area creation. When setting
hotkeys, you can use the up and down arrows (up,down), numbers, and Latin letters.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`cancel`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Keyboard shortcut for canceling area creation.</p>
`confirm`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Keyboard shortcut for confirming area creation.</p>
`labels`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[str\]\]\]**|<p>Keyboard shortcuts for choosing area types. They&#x27;re assigned to buttons in the order they are shown if you enabled the option to choose multiple area types.</p>
`modes`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Mode](toloka.client.project.template_builder.plugins.ImageAnnotationHotkeysPluginV1.Mode.md)\]\]**|<p>Keyboard shortcuts for choosing selection modes.</p>
