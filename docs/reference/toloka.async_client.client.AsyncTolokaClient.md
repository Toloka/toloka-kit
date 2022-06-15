# AsyncTolokaClient
`toloka.async_client.client.AsyncTolokaClient` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/async_client/client.py#L14)

```python
AsyncTolokaClient(
    self,
    *args,
    **kwargs
)
```

Class that implements interaction with [Toloka API](https://toloka.ai/docs/api/concepts/about.html), in an asynchronous way.


All methods are wrapped as async. So all methods calls must be awaited.
All arguments, same as in TolokaClient.

## Methods Summary

| Method | Description |
| :------| :-----------|
[from_sync_client](toloka.async_client.client.AsyncTolokaClient.from_sync_client.md)| None
[wait_operation](toloka.async_client.client.AsyncTolokaClient.wait_operation.md)| Asynchronous version of wait_operation
