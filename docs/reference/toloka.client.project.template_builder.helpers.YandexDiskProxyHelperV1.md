# YandexDiskProxyHelperV1
`toloka.client.project.template_builder.helpers.YandexDiskProxyHelperV1`

```
YandexDiskProxyHelperV1(
    self,
    path: Optional[Union[BaseComponent, str]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

You can use this component to download files from Yandex.Disk.


To use YandexDiskProxyHelper, connect Yandex.Disk to your Toloka account and add the proxy by following
the instructions: [https://yandex.com/support/toloka-requester/concepts/prepare-data.html?lang=en](https://yandex.com/support/toloka-requester/concepts/prepare-data.html?lang=en)
Select the component that you want to add, such as view.image for an image or view.audio for an audio file.
In the url property of this component, use YandexDiskProxyHelper.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`path`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>Path to the file in the /&amp;lt;Proxy name&amp;gt;/&amp;lt;File name&amp;gt;.&amp;lt;type&amp;gt; format</p>
