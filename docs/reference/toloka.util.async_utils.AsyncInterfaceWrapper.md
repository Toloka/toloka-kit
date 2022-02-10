# AsyncInterfaceWrapper
`toloka.util.async_utils.AsyncInterfaceWrapper`

```python
AsyncInterfaceWrapper(self, wrapped: TypeVar('T'))
```

Wrap arbitrary object to be able to await any of it's methods even if it's sync.


Note, that it doesn't provide concurrency by itself!
It just allow to treat sync and async callables in the same way.

