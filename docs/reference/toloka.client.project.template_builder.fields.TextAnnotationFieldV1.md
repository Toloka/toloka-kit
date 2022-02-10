# TextAnnotationFieldV1
`toloka.client.project.template_builder.fields.TextAnnotationFieldV1`

```python
TextAnnotationFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    adjust: Optional[Union[BaseComponent, str]] = None,
    content: Optional[Union[BaseComponent, str]] = None,
    disabled: Optional[Union[BaseComponent, bool]] = None,
    labels: Optional[Union[BaseComponent, List[Union[BaseComponent, Label]]]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component for text segmentation.


Use it to select multiple words, individual words, or letters in the text and label them with values. You can create
multiple categories to label parts of the text, like all nouns and adjectives.

You can use plugin.field.text-annotation.hotkeys to assign keyboard shortcuts for selecting categories.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`adjust`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>If the property value is set to words, only words can be selected in the text. If you don&#x27;t use this property, any part of a line can be selected.</p>
`content`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The text where the performer has to select part of a line.</p>
`disabled`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>This property blocks the component. If true, the component is unavailable to the performer. The default value is false.</p>
`labels`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Label](toloka.client.project.template_builder.fields.TextAnnotationFieldV1.Label.md)\]\]\]\]**|<p>A category.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
