# CompareLayoutV1
`toloka.client.project.template_builder.layouts.CompareLayoutV1`

```
CompareLayoutV1(
    self,
    common_controls: Optional[BaseComponent] = None,
    items: Optional[Union[BaseComponent, List[Union[BaseComponent, CompareLayoutItem]]]] = None,
    *,
    min_width: Optional[Union[BaseComponent, float]] = None,
    wide_common_controls: Optional[Union[BaseComponent, bool]] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Use it to arrange interface elements for comparing them. For example, you can compare several photos.


Selection buttons can be placed under each of the compared items. You can also add common elements, such as a
field for comments.

Differences from layout.side-by-side:

* No buttons for hiding items. These are useful if you need to compare 5 photos at once and it's
difficult to choose between two of them.
* You can add individual selection buttons for every item being compared.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`common_controls`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The common fields of the component. Add information blocks that are common to all the elements being compared.</p>
`items`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [CompareLayoutItem](toloka.client.project.template_builder.layouts.CompareLayoutItem.md)\]\]\]\]**|<p>An array with properties of the elements being compared. Set the appearance of the component blocks.</p>
`min_width`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Minimum width of the element in pixels. Default: 400 pixels.</p>
`wide_common_controls`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>This property increases the common field size of the elements being compared. It&#x27;s set to false by default: the common fields are displayed in the center, not stretched. If true, the fields are wider than with the default value.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
