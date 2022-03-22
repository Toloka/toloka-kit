# LinkOpenedConditionV1
`toloka.client.project.template_builder.conditions.LinkOpenedConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/conditions.py#L166)

```python
LinkOpenedConditionV1(
    self,
    url: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks that the user clicked the link.


Important: To trigger the condition, the user must follow the link from the Toloka interface — you must give users
this option. The condition will not work if the user opens the link from the browser address bar.

This condition can be used in the view.link component and also anywhere you can use (conditions).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`url`|**Optional\[Any\]**|<p>The link that must be clicked.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
