# TriggerPluginV1
`toloka.client.project.template_builder.plugins.TriggerPluginV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/template_builder/plugins.py#L137)

```python
TriggerPluginV1(
    self,
    *,
    action: Optional[BaseComponent] = None,
    condition: Optional[BaseComponent] = None,
    fire_immediately: Optional[Union[BaseComponent, bool]] = None,
    on_change_of: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Use this to configure triggers that trigger a specific action when an event occurs.


The action is set in the action property, and the event is described in the other fields.

The event can be triggered immediately when the task is loaded ("fireImmediately": true) or when data changes in
the property specified in onChangeOf.

You can also set conditions in the conditions property that must be met in order for the trigger to fire.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`action`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The action to perform when the trigger fires.</p>
`condition`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The condition that must be met in order to fire the trigger.</p>
`fire_immediately`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), bool\]\]**|<p>Flag indicating whether the trigger should be fired immediately after the task is loaded.</p>
`on_change_of`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>The data that triggers the action when changed.</p>

**Examples:**

How to save the performer coordinates to the output.

```python
coordinates_save_plugin = tb.plugins.TriggerPluginV1(
    fire_immediately=True,
    action=tb.actions.SetActionV1(
        data=tb.data.OutputData(path='performer_coordinates'),
        payload=tb.data.LocationData()
    ),
)
```
