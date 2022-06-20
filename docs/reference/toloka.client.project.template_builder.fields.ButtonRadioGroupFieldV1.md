# ButtonRadioGroupFieldV1
`toloka.client.project.template_builder.fields.ButtonRadioGroupFieldV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/fields.py#L115)

```python
ButtonRadioGroupFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component with buttons that allow the user to choose between the specified values.


The minimum number of elements is one. Any type of data can be returned.

The size of the button is determined by the length of the text on it.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`options`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [GroupFieldOption](toloka.client.project.template_builder.fields.GroupFieldOption.md)\]\]\]\]**|<p>Array of information about the buttons.</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>

**Examples:**

How to add buttons for classification task.

```python
classification_buttons = tb.fields.ButtonRadioGroupFieldV1(
    tb.data.OutputData(path='class'),
    [
        tb.fields.GroupFieldOption('Cat', 'cat'),
        tb.fields.GroupFieldOption('Dog', 'dog'),
    ],
    validation=tb.conditions.RequiredConditionV1(hint='Choose one of the answer options'),
)
```
