# add_requester_translation
`toloka.client.project.Project.add_requester_translation` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/project/__init__.py#L207)

```python
add_requester_translation(
    self,
    language: str,
    public_name: Optional[str] = None,
    public_description: Optional[str] = None,
    public_instructions: Optional[str] = None
)
```

Add new translations to other language.


You can call it several times for different languages.
If you call it for the same language, it overwrites new values, but don't overwrite values, that you don't pass.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`language`|**str**|<p>Target language. A string from ISO 639-1.</p>
`public_name`|**Optional\[str\]**|<p>Translation of the project name.</p>
`public_description`|**Optional\[str\]**|<p>Translation of the project description.</p>
`public_instructions`|**Optional\[str\]**|<p>Translation of instructions for completing tasks.</p>

**Examples:**

How to add russian translation to the project:

```python
project = toloka.Project(
    public_name='cats vs dogs',
    public_description='image classification',
    public_instructions='do it pls',
    ...
)
project.set_default_language('EN')
project.add_requester_translation(
    language='RU',
    public_name='кошки против собак'
    public_description='классификация изображений'
)
project.add_requester_translation(language='RU', public_instructions='сделай это, пожалуйста')
```
