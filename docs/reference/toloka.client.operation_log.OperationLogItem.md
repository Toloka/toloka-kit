# OperationLogItem
`toloka.client.operation_log.OperationLogItem`

```
OperationLogItem(
    self,
    *,
    type: Optional[str] = None,
    success: Optional[bool] = None,
    input: Optional[Dict[str, Any]] = None,
    output: Optional[Dict[str, Any]] = None
)
```

Objects of which the operation log consists


Contains information about the validation errors and what sets of objects were created.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`type`|**Optional\[str\]**|<p>Type of action in the operation step.</p>
`success`|**Optional\[bool\]**|<p>Result of the step (true or false).</p>
`input`|**Optional\[Dict\[str, Any\]\]**|<p>Input data at the operation step.</p>
`output`|**Optional\[Dict\[str, Any\]\]**|<p>Operation step output. Depends on the type.</p>
