# ensure_async
`toloka.util.async_utils.ensure_async` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/util/async_utils.py#L61)

```python
ensure_async(func: Callable)
```

Ensure given callable is async.


Note, that it doesn't provide concurrency by itself!
It just allow to treat sync and async callables in the same way.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`func`|**Callable**|<p>Any callable: synchronous or asynchronous.</p>

* **Returns:**

  Wrapper that return awaitable object at call.

* **Return type:**

  Callable\[..., Awaitable\]
