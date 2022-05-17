# AudioViewV1
`toloka.client.project.template_builder.view.AudioViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/view.py#L107)

```python
AudioViewV1(
    self,
    url: Optional[Any] = None,
    *,
    loop: Optional[Union[BaseComponent, bool]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

The component plays audio.


Format support depends on the user's browser, OS, and device. We recommend using MP3.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`url`|**Optional\[Any\]**|<p>Audio link.</p>
`loop`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Automatically replay audio.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
