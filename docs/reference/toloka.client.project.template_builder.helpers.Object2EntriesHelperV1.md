# Object2EntriesHelperV1
`toloka.client.project.template_builder.helpers.Object2EntriesHelperV1`

```
Object2EntriesHelperV1(
    self,
    data: Optional[Any] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Creating an array of key-value pairs from the specified object.


For example, let's say you have an object that looks like this:
{
    "foo": "hello",
    "bar": "world"
}
It will be converted to an array whose objects will pair data from the source object and their designations:
[
    {
        "key": "foo",
        "value": "hello"
    },
    {
        "key": "bar",
        "value": "world"
    }
]

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`data`|**Optional\[Any\]**|<p>The object to convert.</p>
