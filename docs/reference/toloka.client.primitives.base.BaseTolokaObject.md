# BaseTolokaObject
`toloka.client.primitives.base.BaseTolokaObject` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/primitives/base.py#L146)

```python
BaseTolokaObject(self)
```

A base class for classes representing Toloka objects.


Subclasses of BaseTolokaObject will:
* Automatically convert annotated attributes attributes via attrs making them optional
  if not explicitly configured otherwise
* Skip missing optional fields during unstructuring with client's cattr converter

## Methods summary

| Method | Description |
| :------| :-----------|
[from_json](toloka.client.primitives.base.BaseTolokaObject.from_json.md)| None
[get_spec_subclass_for_value](toloka.client.primitives.base.BaseTolokaObject.get_spec_subclass_for_value.md)| None
[get_variant_specs](toloka.client.primitives.base.BaseTolokaObject.get_variant_specs.md)| None
[is_variant_base](toloka.client.primitives.base.BaseTolokaObject.is_variant_base.md)| None
[is_variant_incomplete](toloka.client.primitives.base.BaseTolokaObject.is_variant_incomplete.md)| None
[is_variant_spec](toloka.client.primitives.base.BaseTolokaObject.is_variant_spec.md)| None
[to_json](toloka.client.primitives.base.BaseTolokaObject.to_json.md)| None
