# ImageViewV1
`toloka.client.project.template_builder.view.ImageViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/view.py#L211)

```python
ImageViewV1(
    self,
    url: Optional[Any] = None,
    *,
    full_height: Optional[Union[BaseComponent, bool]] = None,
    max_width: Optional[Union[BaseComponent, float]] = None,
    min_width: Optional[Union[BaseComponent, float]] = None,
    no_border: Optional[Union[BaseComponent, bool]] = None,
    no_lazy_load: Optional[Union[BaseComponent, bool]] = None,
    popup: Optional[Union[BaseComponent, bool]] = None,
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = None,
    rotatable: Optional[Union[BaseComponent, bool]] = None,
    scrollable: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Displays an image.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`url`|**Optional\[Any\]**|<p>Image link.</p>
`full_height`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, the element takes up all the vertical free space. The element is set to a minimum height of 400 pixels.</p>
`max_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Maximum width of the element in pixels, must be greater than min_width.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Minimum width of the element in pixels. Takes priority over max_width.</p>
`no_border`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Controls the display of a frame around an image. By default, true (the frame is hidden). Set false to display the frame.</p>
`no_lazy_load`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Disables lazy loading. If true, images start loading immediately, even if they aren&#x27;t in the viewport. Useful for icons. By default, false (lazy loading is enabled). In this mode, images start loading only when they get in the user&#x27;s field of view.</p>
`popup`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Specifies whether opening a full-size image with a click is allowed. By default, it is true (allowed).</p>
`ratio`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]\]\]**|<p>An array of two numbers that sets the relative dimensions of the sides: width (first number) to height (second number). Not valid if full_height=true.</p>
`scrollable`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>When set to true, an image has scroll bars if it doesn&#x27;t fit in the parent element. If false, the image fits in the parent element and, when clicked, opens in its original size in the module window. Images in SVG format with no size specified always fit in their parent elements.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
