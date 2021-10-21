# TaskBatchCreateResult
`toloka.client.batch_create_results.TaskBatchCreateResult`

```
TaskBatchCreateResult(
    self,
    *,
    items: Optional[Dict[str, Task]] = None,
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]] = None
)
```

The list with the results of the tasks creation operation.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Dict\[str, [Task](toloka.client.task.Task.md)\]\]**|<p>Object with created tasks.</p>
`validation_errors`|**Optional\[Dict\[str, Dict\[str, [FieldValidationError](toloka.client.batch_create_results.FieldValidationError.md)\]\]\]**|<p>Object with errors in tasks. Returned if the parameter is used in the request skip_invalid_items=True.</p>
