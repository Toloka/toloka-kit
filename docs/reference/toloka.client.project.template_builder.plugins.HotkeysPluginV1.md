# HotkeysPluginV1
`toloka.client.project.template_builder.plugins.HotkeysPluginV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/template_builder/plugins.py#L79)

```python
HotkeysPluginV1(
    self,
    *,
    key_a: Optional[Any] = None,
    key_b: Optional[Any] = None,
    key_c: Optional[Any] = None,
    key_d: Optional[Any] = None,
    key_e: Optional[Any] = None,
    key_f: Optional[Any] = None,
    key_g: Optional[Any] = None,
    key_h: Optional[Any] = None,
    key_i: Optional[Any] = None,
    key_j: Optional[Any] = None,
    key_k: Optional[Any] = None,
    key_l: Optional[Any] = None,
    key_m: Optional[Any] = None,
    key_n: Optional[Any] = None,
    key_o: Optional[Any] = None,
    key_p: Optional[Any] = None,
    key_q: Optional[Any] = None,
    key_r: Optional[Any] = None,
    key_s: Optional[Any] = None,
    key_t: Optional[Any] = None,
    key_u: Optional[Any] = None,
    key_v: Optional[Any] = None,
    key_w: Optional[Any] = None,
    key_x: Optional[Any] = None,
    key_y: Optional[Any] = None,
    key_z: Optional[Any] = None,
    key_0: Optional[Any] = None,
    key_1: Optional[Any] = None,
    key_2: Optional[Any] = None,
    key_3: Optional[Any] = None,
    key_4: Optional[Any] = None,
    key_5: Optional[Any] = None,
    key_6: Optional[Any] = None,
    key_7: Optional[Any] = None,
    key_8: Optional[Any] = None,
    key_9: Optional[Any] = None,
    key_up: Optional[Any] = None,
    key_down: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Lets you set keyboard shortcuts for actions.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`key_ + [a-z|0-9|up|down]`|**-**|<p>An action that is triggered when you press the specified keyboard key. The keyboard shortcut is set in the key, and the action is specified in the value</p>

**Examples:**

How to create hotkeys for classification buttons.

```python
hot_keys_plugin = tb.HotkeysPluginV1(
    key_1=tb.SetActionV1(tb.OutputData('result'), 'cat'),
    key_2=tb.SetActionV1(tb.OutputData('result'), 'dog'),
    key_3=tb.SetActionV1(tb.OutputData('result'), 'other'),
)
```
