# Accept
`toloka.client.project.template_builder.fields.MediaFileFieldV1.Accept`

```
Accept(
    self,
    *,
    file_system: Optional[Union[BaseComponent, bool]] = None,
    gallery: Optional[Union[BaseComponent, bool]] = None,
    photo: Optional[Union[BaseComponent, bool]] = None,
    video: Optional[Union[BaseComponent, bool]] = None
)
```

Adds different buttons for four types of uploads.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`file_system`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Adds a button for uploading files from the file manager.</p>
`gallery`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Adds a button for uploading files from the gallery.</p>
`photo`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Adds a button for uploading images.</p>
`video`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Adds a button for uploading videos.</p>
