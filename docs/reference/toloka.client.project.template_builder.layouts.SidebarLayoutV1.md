# SidebarLayoutV1
`toloka.client.project.template_builder.layouts.SidebarLayoutV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/layouts.py#L160)

```python
SidebarLayoutV1(
    self,
    content: Optional[BaseComponent] = None,
    controls: Optional[BaseComponent] = None,
    *,
    controls_width: Optional[Union[BaseComponent, float]] = None,
    extra_controls: Optional[BaseComponent] = None,
    min_width: Optional[Union[BaseComponent, float]] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

An option for placing (layout) items, which lets you arrange on a page:


* The main content block.
* An adjacent panel with controls.

The minWidth property sets the threshold for switching between widescreen and compact modes: when the width of the
layout.sidebar component itself becomes less than the value set by the minWidth property, compact mode is enabled.

In widescreen mode, the control panel is located to the right of the main block.

In compact mode, controls stretch to the entire width and are located under each other.

To add an extra panel with controls, use the extraControls property.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content placed in the main area.</p>
`controls`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content of the control panel.</p>
`controls_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The width of the control panel in widescreen mode. In compact mode, the panel takes up the entire available width. Default: 200 pixels.</p>
`extra_controls`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>An additional panel with controls. Located below the main panel.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>The minimum width, in pixels, for widescreen mode. If the component width becomes less than the specified value, the interface switches to compact mode. Default: 400 pixels.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
