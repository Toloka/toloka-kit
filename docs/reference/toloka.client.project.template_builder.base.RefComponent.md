# RefComponent
`toloka.client.project.template_builder.base.RefComponent` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/template_builder/base.py#L191)

```python
RefComponent(self, ref: Optional[str] = None)
```

If you need to insert the same or similar code snippets many times, reuse them.


This helps make your configuration shorter and makes it easier for you to edit duplicate chunks of code.

You can insert a code snippet from another part of the configuration anywhere inside the configuration. To do this,
use the structure RefComponent("path.to.element").

This is useful when you need to insert the same snippet at multiple places in your code. For example, if you need
to run the same action using multiple buttons, put this action in a variable and call it using RefComponent.

