# Field
`toloka.client.pool.dynamic_overlap_config.DynamicOverlapConfig.Field` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/pool/dynamic_overlap_config.py#L39)

```python
Field(self, name: Optional[str] = None)
```

Output data fields to use for aggregating responses.


For best results, each of these fields must
have a limited number of response options.
Don't specify several fields if their values depend on each other.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>The output data field name.</p>
