# set_client
`toloka.metrics.metrics.BaseMetric.set_client` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/metrics/metrics.py#L85)

```python
set_client(self, toloka_client: Union[TolokaClient, AsyncTolokaClient])
```

Sets both TolokaClient and AsyncTolokaClient for the object.


New instance of AsyncTolokaClient is created is case of TolokaClient being passed.

