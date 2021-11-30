# SameDomainConditionV1
`toloka.client.project.template_builder.conditions.SameDomainConditionV1`

```
SameDomainConditionV1(
    self,
    data: Optional[Any] = None,
    original: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    version: Optional[str] = '1.0.0'
)
```

Checks if the link that you entered belongs to a specific site. If it does, returns true, otherwise, false.


Links must be specified in full, including the protocol (http, https, ftp).

The www. subdomain is ignored when checking, meaning that links to www.example.ru and example.ru are considered
to be the same.

How to pass a link address:

* Specify it explicitly as a string.
* (../operations/work-with-data. dita).
* Refer to another element using $ref.
* Use helpers and conditions to get the value.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>The link address to be checked. If you don&#x27;t specify it, the value returned by the parent component (the one that contains condition.same-domain) is used.</p>
`original`|**Optional\[Any\]**|<p>The link address that your link is compared to.</p>
`hint`|**Optional\[Any\]**|<p>Validation error message that the user will see.</p>
