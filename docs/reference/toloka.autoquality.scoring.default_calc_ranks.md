# default_calc_ranks
`toloka.autoquality.scoring.default_calc_ranks` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/autoquality/scoring.py#L111)

```python
default_calc_ranks(scores_df: DataFrame)
```

Calculate default pool ranks for autoquality

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`scores_df`|**DataFrame**|<p>pandas.DataFrame with `pool_id` column and columns with scores from `default_calc_scores`</p>

* **Returns:**

  input DataFrame with an additional ranks columns

* **Return type:**

  DataFrame
