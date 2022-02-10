# ListFieldV1
`toloka.client.project.template_builder.fields.ListFieldV1`

```python
ListFieldV1(
    self,
    data: Optional[BaseComponent] = None,
    render: Optional[BaseComponent] = None,
    *,
    button_label: Optional[Any] = None,
    direction: Optional[Union[BaseComponent, ListDirection]] = None,
    editable: Optional[Union[BaseComponent, bool]] = None,
    max_length: Optional[Union[BaseComponent, float]] = None,
    size: Optional[Union[BaseComponent, ListSize]] = None,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

A component that allows the user to add and remove list items, such as text fields to fill in.


This way you can allow the user to give multiple answers to a question.

The list items can contain any component, including a list of other components. For example, this allows you to
create a table where you can add and delete rows.

To add a new list item, the user clicks the button. To remove an item, they click on the x on the right (it appears
when hovering over a list item).

To prevent the user from adding too many list items, set the maximum list length. You can also use the editable
property to block users from changing a component, like when a certain event occurs.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Data with values that will be processed or changed.</p>
`render`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Interface template for list items, such as a text field. In nested field.* components, use data.relative for recording responses, otherwise all the list items will have the same value.</p>
`button_label`|**Optional\[Any\]**|<p>Text on the button for adding list items.</p>
`direction`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [ListDirection](toloka.client.project.template_builder.base.ListDirection.md)\]\]**|<p>The direction of the list.</p>
`editable`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>A property that indicates whether adding and removing list items is allowed. Set false to disable. By default it is true (allowed).</p>
`max_length`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), float\]\]**|<p>Maximum number of list items.</p>
`size`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), [ListSize](toloka.client.project.template_builder.base.ListSize.md)\]\]**|<p>The distance between list items. Acceptable values in ascending order: s, m (default).</p>
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
