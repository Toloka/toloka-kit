# PlayedFullyConditionV1
`toloka.client.project.template_builder.conditions.PlayedFullyConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/conditions.py#L204)

```python
PlayedFullyConditionV1(
    self,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

This component checks for the end of playback.


Validation is passed if playback is finished. To play media with the condition.played-fully check, you can use
view.audio and view.video. The condition.played-fully check only works in the player's validation property.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
