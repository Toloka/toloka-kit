# SwitchHelperV1
`toloka.client.project.template_builder.helpers.SwitchHelperV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/helpers.py#L187)

```python
SwitchHelperV1(
    self,
    cases: Optional[Union[BaseComponent, List[Union[BaseComponent, Case]]]] = None,
    default: Optional[Any] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

A switch-case construction.


Checks various conditions sequentially and executes the code from the result property when the corresponding
condition is true.

You can use it to perform an action or display an additional interface element only when a certain condition is met.
View example in the sandbox.

This helper is similar to a series of If...Then...Else logical expressions, so it is useful if there are more than
two conditions for sequential verification. If you need to check one or two conditions, use the helper.if component.
How the helper works:
    * The helper checks (conditions) from the array of cases objects, starting from the first one.
    * If the condition is true (returns true), the helper returns the result (block of code) specified in the result
      property for the condition object in the cases array. The helper quits and subsequent conditions are not
      checked.
    * If the condition is false (returns false), the helper checks the subsequent condition.
    * If all conditions are false as a result of all checks, the helper returns the value specified in the default
      property (if it is not defined, the helper returns nothing).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`cases`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), List\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [Case](toloka.client.project.template_builder.helpers.SwitchHelperV1.Case.md)\]\]\]\]**|<p>An array of objects consisting of condition and result property pairs.</p>
`default`|**Optional\[Any\]**|<p>Element that is returned if none of the checked conditions returned true.</p>
