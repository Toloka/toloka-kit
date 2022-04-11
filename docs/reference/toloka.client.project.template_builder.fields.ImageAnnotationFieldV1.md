# ImageAnnotationFieldV1
`toloka.client.project.template_builder.fields.ImageAnnotationFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/fields.py#L248)

```python
ImageAnnotationFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    image: Optional[Union[BaseComponent, str]] = None,
    *,
    disabled: Optional[Union[BaseComponent, bool]] = None,
    full_height: Optional[Union[BaseComponent, bool]] = None,
    labels: Optional[Union[BaseComponent, List[Union[BaseComponent, Label]]]] = None,
    min_width: Optional[Union[BaseComponent, float]] = None,
    ratio: Optional[Union[BaseComponent, List[Union[BaseComponent, float]]]] = None,
    shapes: Optional[Union[BaseComponent, Dict[Union[BaseComponent, Shape], Union[BaseComponent, bool]]]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Adds an interface for selecting areas in images.


If you need to select different types of objects, classify the areas using the labels property.

You can select areas using points, polygons, and rectangles. In the shapes property, you can keep some of the
selection modes and hide the rest.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`image`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The image you want to select areas in.</p>
`disabled`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Determines whether adding and deleting areas is allowed:<ul><li>false (default) — Allowed.</li><li>true — Not allowed. You can use this feature when creating an interface to check whether the selection is correct,  or if you need to allow selection only when a certain condition is met.</li></ul></p>
`full_height`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, the element takes up all the vertical free space. The element is set to a minimum height of 400 pixels.</p>
`labels`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Label](toloka.client.project.template_builder.fields.ImageAnnotationFieldV1.Label.md)\]\]\]\]**|<p>Used to classify areas. You can add several area types. When adding an area type, a button to select it appears in the interface, and when setting a new value, a new area selection color is added. This feature is instrumental if you need to select different types of objects: you can use one color to select cars and a different one for pedestrians.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Minimum width of the element in pixels. Takes priority over max_width.</p>
`ratio`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]\]\]**|<p>An array of two numbers that sets the relative dimensions of the sides: width (first number) to height (second number). Not valid if full_height=true.</p>
`shapes`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), Dict\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Shape](toloka.client.project.template_builder.fields.ImageAnnotationFieldV1.Shape.md)\], Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]\]\]**|<p>Used to add and hide selection modes: points, polygons, and rectangles. All three modes are available by default. Use this property if you only need to keep certain modes. Modes with the true value are available.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
