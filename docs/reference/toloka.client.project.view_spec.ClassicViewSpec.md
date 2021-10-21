# ClassicViewSpec
`toloka.client.project.view_spec.ClassicViewSpec`

```
ClassicViewSpec(
    self,
    *,
    settings: Optional[ViewSpec.Settings] = None,
    script: Optional[str] = None,
    markup: Optional[str] = None,
    styles: Optional[str] = None,
    assets: Optional[Assets] = None
)
```

A classic view specification defined with HTML, CSS and JS.


For more information, see Toloka Requester's guide
[https://yandex.ru/support/toloka-requester/?lang=en](https://yandex.ru/support/toloka-requester/?lang=en)

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`script`|**Optional\[str\]**|<p>JavaScript interface for the task.</p>
`markup`|**Optional\[str\]**|<p>Task interface.</p>
`styles`|**Optional\[str\]**|<p>CSS task interface.</p>
`assets`|**Optional\[[Assets](toloka.client.project.view_spec.ClassicViewSpec.Assets.md)\]**|<p>Linked files such as:<ul><li>CSS styles</li><li>JavaScript libraries</li><li>Toloka assets with the $TOLOKA_ASSETS prefix Add items in the order they should be linked when running the task interface.</li></ul></p>
