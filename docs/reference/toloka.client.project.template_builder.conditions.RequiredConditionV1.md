# RequiredConditionV1
`toloka.client.project.template_builder.conditions.RequiredConditionV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/conditions.py#L215)

```python
RequiredConditionV1(
    self,
    data: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks that the data is filled in. This way you can get the user to answer all the required questions.


If used inside the validation property, you can omit the data property and the same property will be used from the
parent component field (the one that contains the condition.required component).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>Data to be filled in. If the property is not specified, the data of the parent component (the one that contains condition.required) is used.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>

**Examples:**

How to check that image is uploaded.

```python
image = tb.fields.MediaFileFieldV1(
    tb.data.OutputData('image'),
    tb.fields.MediaFileFieldV1.Accept(photo=True, gallery=True),
    validation=tb.conditions.RequiredConditionV1(hint='Your must upload photo.'),
)
```
