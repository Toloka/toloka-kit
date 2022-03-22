# MarkdownViewV1
`toloka.client.project.template_builder.view.MarkdownViewV1` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/view.py#L358)

```python
MarkdownViewV1(
    self,
    content: Optional[Any] = None,
    *,
    hint: Optional[Any] = None,
    label: Optional[Any] = None,
    validation: Optional[BaseComponent] = None,
    version: Optional[str] = '1.0.0'
)
```

Block for displaying text in Markdown.


The contents of the block are written to the content property in a single line. To insert line breaks, use \n
    Straight quotation marks (") must be escaped like this: \".

    Note that the view.markdown component is resource-intensive and might overload weak user devices.
    Do not use this component to display plain text. If you need to display text without formatting, use the view.text
    component. If you need to insert a link, use view.link, and for an image use view.image.
    Links with Markdown are appended with target="_blank" (the link opens in a new tab), as well as
    rel="noopener noreferrer"

    Attributes:
        content: Text in Markdown.

    Example:
        How to add a title and description on the task interface.

        >>> header = tb.view.MarkdownViewV1('# Some Header:
---
Some detailed description')
        ...

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`hint`|**Optional\[Any\]**|<p>Hint text.</p>
`label`|**Optional\[Any\]**|<p>Label above the component.</p>
`validation`|**Optional\[[BaseComponent](toloka.client.project.template_builder.base.BaseComponent.md)\]**|<p>Validation based on condition.</p>
