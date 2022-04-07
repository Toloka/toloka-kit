# AsyncInterfaceWrapper
`toloka.util.async_utils.AsyncInterfaceWrapper` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/util/async_utils.py#L81)

```python
AsyncInterfaceWrapper(self, wrapped: TypeVar('T'))
```

Wrap arbitrary object to be able to await any of it's methods even if it's sync.


Note, that it doesn't provide concurrency by itself!
It just allow to treat sync and async callables in the same way.

