# Assets
`toloka.client.project.view_spec.ClassicViewSpec.Assets` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.26/src/client/project/view_spec.py#L80)

```python
Assets(
    self,
    *,
    style_urls: Optional[List[str]] = None,
    script_urls: Optional[List[str]] = None
)
```

Linked files with assets.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`style_urls`|**Optional\[List\[str\]\]**|<p>Links to CSS libraries.</p>
`script_urls`|**Optional\[List\[str\]\]**|<p>Links to JavaScript libraries and Toloka assets. Toloka assets:<ul><li>&quot;$TOLOKA_ASSETS/js/toloka-handlebars-templates.js&quot; — Handlebars. See the description on the template     engine website [here](http://handlebarsjs.com/)</li><li>&quot;$TOLOKA_ASSETS/js/image-annotation.js&quot; — Image labeling interface. See image with area selection in     the Requester&#x27;s guide [here](https://yandex.ru/support/toloka-requester/concepts/t-components/image-annotation.html/?lang=en) Note that the image labeling interface should only be connected together with the Handlebars helpers. The order of connection matters.</li></ul></p>

**Examples:**

```python
from toloka.client.project.view_spec import ClassicViewSpec
view_spec = ClassicViewSpec(
    ...,
    assets = ClassicViewSpec.Assets(
        script_utls = [
            "$TOLOKA_ASSETS/js/toloka-handlebars-templates.js",
            "$TOLOKA_ASSETS/js/image-annotation.js",
        ]
    )
)
```
