# get_operation
`toloka.client.TolokaClient.get_operation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/__init__.py#L44)

```python
get_operation(self, operation_id: str)
```

Reads information about operation


All asynchronous actions in Toloka works via operations. If you have some "Operation" usually you need to use
"wait_operation" method.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operation_id`|**str**|<p>ID of the operation.</p>

* **Returns:**

  The operation.

* **Return type:**

  [Operation](toloka.client.operations.Operation.md)

**Examples:**

```python
op = toloka_client.get_operation(operation_id='1')
```
