# _AppError
`toloka.client.app._AppError` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/app/__init__.py#L19)

```python
_AppError(
    self,
    *,
    code: Optional[str] = None,
    message: Optional[str] = None,
    payload: Optional[Any] = None
)
```

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`code`|**Optional\[str\]**|<p>String error code.</p>
`message`|**Optional\[str\]**|<p>Detailed description of the error.</p>
`payload`|**Optional\[Any\]**|<p>Additional information about the error. May have different structure for different errors.</p>
