# InfiniteOverlapParametersMixin
`toloka.client.primitives.infinite_overlap.InfiniteOverlapParametersMixin` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/primitives/infinite_overlap.py#L6)

```python
InfiniteOverlapParametersMixin(
    self,
    infinite_overlap=None,
    overlap=None
)
```

This mixin provides `overlap` and `infinite_overlap` attributes


and is responsible for maintaining their consistency.

Possible states:
* `overlap` is None and `infinite_overlap` is None:
    Interpreted as "overlap was not provided"
* `overlap` is None and `infinite_overlap` is True:
    Interpreted as "infinite overlap"
* `overlap` is not None and `infinite_overlap` is False:
    Interpreted as "finite overlap of `overlap`"

All other states are considered invalid

## Methods summary

| Method | Description |
| :------| :-----------|
[unset_overlap](toloka.client.primitives.infinite_overlap.InfiniteOverlapParametersMixin.unset_overlap.md)| Unsets overlap
