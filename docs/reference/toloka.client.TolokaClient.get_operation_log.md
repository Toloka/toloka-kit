# get_operation_log
`toloka.client.TolokaClient.get_operation_log` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
get_operation_log(self, operation_id: str)
```

Reads information about validation errors and which task (or task suites) were created


You don't need to call this method if you use "create_tasks" for creating tasks ("create_task_suites" for task suites).
By asynchronous creating multiple tasks (or task sets) you can get the operation log.
Logs are only available for the last month.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**str**|<p>ID of the operation.</p>

* **Returns:**

  Logs for the operation.

* **Return type:**

  List\[[OperationLogItem](toloka.client.operation_log.OperationLogItem.md)\]

**Examples:**

```python
op = toloka_client.get_operation_log(operation_id='1')
```
