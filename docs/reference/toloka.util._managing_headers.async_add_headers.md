# async_add_headers
`toloka.util._managing_headers.async_add_headers` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/util/_managing_headers.py#L57)

```python
async_add_headers(client: str)
```

This decorator add 3 headers into resulting http request called by async function:


1) X-Caller-Context: high-level abstraction like client, metrics, streaming
2) X-Top-Level-Method: first function, that was called and then called other functions which provoked request
3) X-Low-Level-Method: last function before calling TolokaClient _method (_raw_request for example)

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`client`|**str**|<p>name of high-level abstraction for X-Caller-Context</p>
