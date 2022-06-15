# AsyncMultithreadWrapper
`toloka.util.async_utils.AsyncMultithreadWrapper` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/util/async_utils.py#L103)

```python
AsyncMultithreadWrapper(
    self,
    wrapped: TypeVar('T'),
    pool_size: int = 10,
    loop: Optional[AbstractEventLoop] = None
)
```

Wrap arbitrary object to run each of it's methods in a separate thread.


**Examples:**

Simple usage example.

```python
class SyncClassExample:
    def sync_method(self, sec):
        time.sleep(sec)  # Definitely not async.
        return sec
obj = AsyncMultithreadWrapper(SyncClassExample())
await asyncio.gather(*[obj.sync_method(1) for _ in range(10)])
```
