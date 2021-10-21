# OpenCloseActionV1
`toloka.client.project.template_builder.actions.OpenCloseActionV1`

```
OpenCloseActionV1(
    self,
    view: Optional[Union[BaseComponent, RefComponent]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

This component changes the display mode of another component by opening or closing it.


What happens to the component depends on the type of component:
    view.image — expands the image to full screen.
    view.collapse — expands or collapses a collapsible section of content.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`view`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [RefComponent](toloka.client.project.template_builder.base.RefComponent.md)\]\]**|<p>Points to the component to perform the action with.</p>
