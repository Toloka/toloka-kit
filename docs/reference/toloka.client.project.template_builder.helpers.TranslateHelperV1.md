# TranslateHelperV1
`toloka.client.project.template_builder.helpers.TranslateHelperV1`

```python
TranslateHelperV1(
    self,
    key: Optional[Union[BaseComponent, str]] = None,
    *,
    version: Optional[str] = '1.0.0'
)
```

Component for translating interface elements to other languages.


In the properties that should be displayed in different languages, add:

{
  "type": "helper.translate",
  "key": "<key name>"
{

Adding the key property displays a field for entering the key text. Enter the text in the source language. In the
"Translations" step, add translations for the keys in the desired languages.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`key`|**Optional\[Union\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md), str\]\]**|<p>The key for a text property that you will translate to other languages.</p>
