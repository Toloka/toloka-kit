# BarsLayoutV1
`toloka.client.project.template_builder.layouts.BarsLayoutV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/layouts.py#L39)

```python
BarsLayoutV1(
    self,
    content: Optional[BaseComponent] = None,
    *,
    bar_after: Optional[BaseComponent] = None,
    bar_before: Optional[BaseComponent] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component that adds top and bottom bars to the content.


You can use other components inside each part of this component, such as images, text, or options.

The top bar is located at the top edge of the component, and the bottom one is at the bottom edge. The content is
placed between the bars and takes up all available space.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The main content.</p>
`bar_after`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The bar displayed at the bottom edge of the component.</p>
`bar_before`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The bar displayed at the top edge of the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
