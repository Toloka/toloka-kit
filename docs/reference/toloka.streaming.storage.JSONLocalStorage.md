# JSONLocalStorage
`toloka.streaming.storage.JSONLocalStorage` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/storage.py#L56)

```python
JSONLocalStorage(
    self,
    dirname: str = '/tmp',
    *,
    locker: Optional[BaseLocker] = ...
)
```

Simplest local storage to dump state of a pipeline and restore in case of restart.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`dirname`|**str**|<p>Directory to store pipeline&#x27;s state files. By default, &quot;/tmp&quot;.</p>
`locker`|**Optional\[[BaseLocker](toloka.streaming.locker.BaseLocker.md)\]**|<p>Optional locker object. By default, FileLocker with the same dirname is used.</p>

**Examples:**

Allow pipeline to dump it's state to the local storage.

```python
pipeline = Pipeline(storage=JSONLocalStorage())
...
await pipeline.run()  # Will load from storage at the start and save after each iteration.
```

Set locker explicitly.

```python
storage = JSONLocalStorage('/store-data-here', locker=FileLocker('/store-locks-here'))
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[cleanup](toloka.streaming.storage.JSONLocalStorage.cleanup.md)| None
[load](toloka.streaming.storage.JSONLocalStorage.load.md)| None
[save](toloka.streaming.storage.JSONLocalStorage.save.md)| None
