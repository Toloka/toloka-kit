# AutoQuality
`toloka.autoquality.optimizer.AutoQuality` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/autoquality/optimizer.py#L200)

```python
AutoQuality(
    self,
    toloka_client: TolokaClient,
    project_id: str,
    base_pool_id: str,
    training_pool_id: str,
    exam_pool_id: Optional[str] = None,
    exam_skill_id: Optional[str] = None,
    label_field: str = 'label',
    n_iter: int = 10,
    parameter_distributions: Dict = ...,
    score_func: Callable = default_calc_scores,
    ranking_func: Callable = default_calc_ranks,
    create_autoquality_pool_func: Callable = _create_autoquality_pool_default,
    run_id: str = 'AutoQuality Project 2022-06-10 16:05:10'
)
```

This class implements a tool to help set up quality control for Toloka project.


To use `toloka.autoquality` install toloka-kit via `pip install toloka-kit[autoquality]`

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`toloka_client`|**[TolokaClient](toloka.client.TolokaClient.md)**|<p>TolokaClient instance to interact with requester&#x27;s account</p>
`project_id`|**str**|<p>Toloka project ID</p>
`base_pool_id`|**str**|<p>Temolate Pool for autoquality pools</p>
`training_pool_id`|**str**|<p> Training Pool ID</p>
`exam_pool_id`|**Optional\[str\]**|<p>Exam Pool ID</p>
`exam_skill_id`|**Optional\[str\]**|<p>Skill for filtering by exam perfomance</p>
`label_field`|**str**|<p>Output field name</p>
`n_iter`|**int**|<p>Number of an autoquality pools</p>
`parameter_distributions`|**Dict**|<p>Parameter distributions</p>
`score_func`|**Callable**|<p>Callable to calculate pool scores</p>
`ranking_func`|**Callable**|<p>Callabale to ranking pools based on their scores</p>
`create_autoquality_pool_func`|**Callable**|<p>Callable to create autoquality pool</p>
`run_id`|**str**|<p>ID of autoquality run</p>

**Examples:**

```python
aq = AutoQuality(
  toloka_client=toloka_client,
  project_id=...,
  base_pool_id=...,
  training_pool_id=...,
  exam_pool_id = ...,
  exam_skill_id = ...
)
aq.setup_pools()
aq.create_tasks(aq_tasks)
aq.run()
aq.best_pool_params
```
## Methods Summary

| Method | Description |
| :------| :-----------|
[archive_autoquality_pools](toloka.autoquality.optimizer.AutoQuality.archive_autoquality_pools.md)| Archive all pools created by `AutoQuality.setup_pools`
[create_tasks](toloka.autoquality.optimizer.AutoQuality.create_tasks.md)| Add tasks to autoquality pools.
[run](toloka.autoquality.optimizer.AutoQuality.run.md)| Run autoquality process.
[setup_pools](toloka.autoquality.optimizer.AutoQuality.setup_pools.md)| Create autoquality pools with sampled quality control parameters.
