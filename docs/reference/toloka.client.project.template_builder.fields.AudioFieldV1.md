# AudioFieldV1
`toloka.client.project.template_builder.fields.AudioFieldV1`

```python
AudioFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    *,
    multiple: Optional[Any] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Component for recording audio.


Works in the mobile app. In a browser, this component opens a window for uploading an audio file.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`multiple`|**Optional\[Any\]**|<p>Determines whether multiple audio files can be recorded (or uploaded): False (default) — forbidden. True — allowed.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
