# ZooKeeperLocker
`toloka.streaming.locker.ZooKeeperLocker`

```python
ZooKeeperLocker(
    self,
    client: KazooClient,
    dirname: str,
    timeout: Optional[int] = None,
    identifier: str = 'lock'
)
```

Apache ZooKeeper-based locker to use with a storage.


Two locks cannot be taken simultaneously with the same key.
If the instance detects that the lock was taken by a newer version, it throws an error.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`client`|**KazooClient**|<p>KazooClient object.</p>
`dirname`|**str**|<p>Base node path to put locks in.</p>
`timeout`|**Optional\[int\]**|<p>Time in seconds to wait in case of lock being already acquired. Infinite by default.</p>
`identifier`|**str**|<p>Optional lock identifier.</p>

**Examples:**

Create lock object.

```python
!pip install kazoo
from kazoo.client import KazooClient
zk = KazooClient('127.0.0.1:2181')
zk.start()
locker = ZooKeeperLocker(zk, '/my-locks')
```

Try to lock the same key at the same time..

```python
locker_1 = ZooKeeperLocker(zk, '/locks')
locker_2 = ZooKeeperLocker(zk, '/locks', timeout=0)
with locker_1('some_key') as lock_1:
    with locker_2('some_key') as lock_2:  # => raise an error: timeout
        pass
```

Try to lock the same key sequentially.

```python
locker_1 = ZooKeeperLocker(zk, '/locks')
locker_2 = ZooKeeperLocker(zk, '/locks')
with locker_1('some_key'):
    pass
with locker_2('some_key'):
    pass
with locker_1('some_key'):  # raise an error: NewerInstanceDetectedError
    pass
```
