# CollectorConfig
`toloka.client.collectors.CollectorConfig`

```
CollectorConfig(self, *, uuid: Optional[UUID] = None)
```

Base class for all collectors


Attriutes:
    uuid: Id for this collector. Pay attention! If you clone the pool, you will have same collector in old and new pools.
        So collectors can behave a little unexpectedly. For example they start gather "history_size" patameter
        from both pools.

## Methods summary

| Method | Description |
| :------| :-----------|
[validate_condition](toloka.client.collectors.CollectorConfig.validate_condition.md)| None
