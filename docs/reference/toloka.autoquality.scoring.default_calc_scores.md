# default_calc_scores
`toloka.autoquality.scoring.default_calc_scores` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/autoquality/scoring.py#L18)

```python
default_calc_scores(
    toloka_client: TolokaClient,
    pool_id: str,
    label_field: str
)
```

Calculate default scores for Autoquality.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**[TolokaClient](toloka.client.TolokaClient.md)**|<p>`TolokaClient` instance to interact with requester&#x27;s account</p>
`pool_id`|**str**|<p>Pool ID to calculate scores for</p>
`label_field`|**str**|<p>Target output field</p>

* **Returns:**

  Dict with scores

* **Return type:**

  Dict\[str, Any\]
