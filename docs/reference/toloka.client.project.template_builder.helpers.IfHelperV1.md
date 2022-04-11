# IfHelperV1
`toloka.client.project.template_builder.helpers.IfHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/helpers.py#L72)

```python
IfHelperV1(
    self,
    condition: Optional[BaseComponent] = None,
    then: Optional[Any] = None,
    *,
    else_: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

The If...Then...Else operator.


Allows you to execute either one block of code or another, depending on the condition. If you need more options,
use helper.switch.

For example, if you want to conduct a survey, you can use the helper.if component to ask the gender of the
respondent and add different sets of questions, depending on whether the respondent is male or female.
How it works: If the condition in if is true (returns true), the code specified in the then property will be
executed. Otherwise (the condition is false and returns false) the code specified in else will be executed.
The else property is optional. For example, let's say you ask the user " did you Like the image". You can make a
comment field appear when a negative response is received, but nothing happens when a positive response is received.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`condition`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Condition to check.</p>
`then`|**Optional\[Any\]**|<p>The element that is returned if the condition from the condition property is true (returns true).</p>
`else_`|**Optional\[Any\]**|<p>The element that is returned if the condition from the condition property is false (returns false).</p>

**Examples:**

How to show a part of the interface by condition.

```python
hidden_ui = tb.helpers.IfHelperV1(
    tb.conditions.EqualsConditionV1(tb.data.OutputData('show_me'), 'show'),
    tb.view.ListViewV1([header, buttons, images]),
)
```
