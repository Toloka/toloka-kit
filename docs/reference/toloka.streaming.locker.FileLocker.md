# FileLocker
`toloka.streaming.locker.FileLocker` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/streaming/locker.py#L49)

```python
FileLocker(
    self,
    dirname: str = '/tmp',
    timeout: Optional[int] = None
)
```

Simplest filesystem-based locker to use with a storage.


Two locks cannot be taken simultaneously with the same key.
If the instance detects that the lock was taken by a newer version, it throws an error.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`dirname`|**str**|<p>Directory to store lock files ending with &quot;.lock&quot; and &quot;.lock.content&quot;.</p>
`timeout`|**Optional\[int\]**|<p>Time in seconds to wait in case of lock being already acquired. Infinite by default.</p>

**Examples:**

Try to lock the same key at the same time..

```python
locker_1 = FileLocker()
locker_2 = FileLocker(timeout=0)
with locker_1('some_key') as lock_1:
    with locker_2('some_key') as lock_2:  # => raise an error: timeout
        pass
```

Try to lock the same key sequentially.

```python
locker_1 = FileLocker()
locker_2 = FileLocker()
with locker_1('some_key'):
    pass
with locker_2('some_key'):
    pass
with locker_1('some_key'):  # raise an error: NewerInstanceDetectedError
    pass
```
## Methods summary

| Method | Description |
| :------| :-----------|
[cleanup](toloka.streaming.locker.FileLocker.cleanup.md)| None
