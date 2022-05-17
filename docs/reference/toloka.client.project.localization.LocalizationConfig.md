# LocalizationConfig
`toloka.client.project.localization.LocalizationConfig` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/project/localization.py#L47)

```python
LocalizationConfig(
    self,
    *,
    default_language: Optional[str] = None,
    additional_languages: Optional[List[AdditionalLanguage]] = ...
)
```

Translates the part of the project visible to the performers into different languages


It is used to make it easier for performers from other countries who do not speak the necessary language to
understand and perform tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`default_language`|**Optional\[str\]**|<p>The source language used in the fields public_name, public_description, and public_instructions. Required parameter.</p>
`additional_languages`|**Optional\[List\[[AdditionalLanguage](toloka.client.project.localization.AdditionalLanguage.md)\]\]**|<p>List of translations into other languages. One element - one translation.</p>
