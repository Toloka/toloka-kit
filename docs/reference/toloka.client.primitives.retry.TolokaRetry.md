# TolokaRetry
`toloka.client.primitives.retry.TolokaRetry` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/primitives/retry.py#L17)

```python
TolokaRetry(
    self,
    *args,
    retry_quotas: Union[List[str], str, None] = 'MIN',
    **kwargs
)
```

Retry toloka quotas. By default only minutes quotas.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`retry_quotas`|**Union\[List\[str\], str, None\]**|<p>List of quotas that will be retried. None or empty list for not retrying quotas. You can specify quotas:<ul><li>MIN - Retry minutes quotas.</li><li>HOUR - Retry hourly quotas. This is means that the program just sleeps for an hour! Be careful.</li><li>DAY - Retry daily quotas. We strongly not recommended retrying these quotas.</li></ul></p>
## Methods summary

| Method | Description |
| :------| :-----------|
[get_retry_after](toloka.client.primitives.retry.TolokaRetry.get_retry_after.md)| None
[increment](toloka.client.primitives.retry.TolokaRetry.increment.md)| None
[new](toloka.client.primitives.retry.TolokaRetry.new.md)| None
