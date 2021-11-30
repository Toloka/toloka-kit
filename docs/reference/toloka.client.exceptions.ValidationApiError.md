# ValidationApiError
`toloka.client.exceptions.ValidationApiError`

Field validation error returned from the API Call.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`status_code`|**Optional\[int\]**|<p>response status code.</p>
`request_id`|**Optional\[str\]**|<p>request ID</p>
`code`|**Optional\[str\]**|<p>error code string</p>
`message`|**Optional\[str\]**|<p>error message</p>
`payload`|**Optional\[Any\]**|<p>additional payload</p>
`invalid_fields`|**-**|<p>the list of the invalid fields</p>
