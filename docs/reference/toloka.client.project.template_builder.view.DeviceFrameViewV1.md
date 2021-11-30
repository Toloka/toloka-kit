# DeviceFrameViewV1
`toloka.client.project.template_builder.view.DeviceFrameViewV1`

```
DeviceFrameViewV1(
    self,
    content: Optional[BaseComponent] = None,
    *,
    full_height: Optional[Union[BaseComponent, bool]] = None,
    max_width: Optional[Union[BaseComponent, float]] = None,
    min_width: Optional[Union[BaseComponent, float]] = None,
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Wraps the content of a component in a frame that is similar to a mobile phone.


You can place other components inside the frame.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content inside the frame.</p>
`full_height`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, the element takes up all the vertical free space. The element is set to a minimum height of 400 pixels.</p>
`max_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Maximum width of the element in pixels, must be greater than min_width.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Minimum width of the element in pixels. Takes priority over max_width.</p>
`ratio`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]\]\]**|<p>An array of two numbers that sets the relative dimensions of the sides: width (first number) to height (second number). Not valid if full_height=true.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
