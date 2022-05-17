# FileFieldV1
`toloka.client.project.template_builder.fields.FileFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/fields.py#L226)

```python
FileFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    accept: Optional[Union[BaseComponent, List[Union[BaseComponent, str]]]] = None,
    *,
    multiple: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

This component can be used for uploading files. It's displayed in the interface as an upload button.


You can restrict the file types to upload in the "accept" property. By default, only one file can be uploaded,
but you can allow multiple files in the "multiple" property.

If a user logs in from a mobile device, it's more convenient to use field.media-file — it's adapted for mobile
devices and makes it easier to upload photos and videos.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`accept`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]\]\]**|<p>A list of file types that can be uploaded. By default, you can upload any files. Specify the types in the [certain format](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types). For example, you can allow only images to be uploaded by adding the image/jpeg and image/png types.</p>
`multiple`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Determines whether multiple files can be uploaded:<ul><li>false (default) — forbidden.</li><li>true — allowed.</li></ul></p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
