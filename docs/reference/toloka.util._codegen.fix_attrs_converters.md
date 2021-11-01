# fix_attrs_converters
`toloka.util._codegen.fix_attrs_converters`

```
fix_attrs_converters(cls)
```

Due to [https://github.com/Toloka/toloka-kit/issues/37](https://github.com/Toloka/toloka-kit/issues/37)


we have to support attrs>=20.3.0.
This version lacks a feature that uses converters' annotations in class's __init__
(see [https://github.com/python-attrs/attrs/pull/710](https://github.com/python-attrs/attrs/pull/710))).
This decorator brings this feature to older attrs versions.

