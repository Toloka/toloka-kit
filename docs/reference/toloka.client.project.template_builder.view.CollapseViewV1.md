# CollapseViewV1
`toloka.client.project.template_builder.view.CollapseViewV1`

```
CollapseViewV1(
    self,
    content: Optional[BaseComponent] = None,
    *,
    label: Optional[Any] = None,
    default_opened: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Expandable block.


Lets you add hidden content that doesn't need to be shown initially or that takes up a large space.

The block heading is always visible.

If you set the defaultOpened property to true, the block is expanded immediately, but it can be collapsed.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`content`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Content hidden in the block.</p>
`label`|**Optional\[Any\]**|<p>Block heading.</p>
`default_opened`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>If true, the block is immediately displayed in expanded form. By default, false (the block is collapsed).</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
