# MediaFileFieldV1
`toloka.client.project.template_builder.fields.MediaFileFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/fields.py#L340)

```python
MediaFileFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    accept: Optional[Union[BaseComponent, Accept]] = None,
    *,
    multiple: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Adds buttons for different types of uploads: uploading photos or videos, selecting files from the file manager or choosing from the gallery. In the accept property, select which buttons you need.


By default, only one file can be uploaded, but you can allow multiple files in the multiple property.

This component is convenient when using mobile devices. To upload files from a computer, it's better to use
field.file for a more flexible configuration of the file types.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`accept`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Accept](toloka.client.project.template_builder.fields.MediaFileFieldV1.Accept.md)\]\]**|<p>Adds different buttons for four types of uploads. Pass the true value for the ones that you need. For example, if you need a button for uploading files from the gallery, add the &quot;gallery&quot;: true property</p>
`multiple`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Determines whether multiple files can be uploaded:</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>

**Examples:**

How to allow performers to upload images and make photos.

```python
image_loader = tb.fields.MediaFileFieldV1(
    label='Upload a photo',
    data=tb.data.OutputData(path='image'),
    validation=tb.conditions.RequiredConditionV1(),
    accept=tb.fields.MediaFileFieldV1.Accept(photo=True, gallery=True),
    multiple=False,
)
```
