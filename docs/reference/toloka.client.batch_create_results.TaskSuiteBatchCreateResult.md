# TaskSuiteBatchCreateResult
`toloka.client.batch_create_results.TaskSuiteBatchCreateResult`

```python
TaskSuiteBatchCreateResult(
    self,
    *,
    items: Optional[Dict[str, TaskSuite]] = None,
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]] = None
)
```

The list with the results of the task suites creation operation.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Dict\[str, [TaskSuite](toloka.client.task_suite.TaskSuite.md)\]\]**|<p>Object with created task suites.</p>
`validation_errors`|**Optional\[Dict\[str, Dict\[str, [FieldValidationError](toloka.client.batch_create_results.FieldValidationError.md)\]\]\]**|<p>Object with errors in task suites. Returned if the parameter is used in the request skip_invalid_items=True.</p>
