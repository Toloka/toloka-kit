# Languages
`toloka.client.filter.Languages`

```python
Languages(
    self,
    operator: InclusionOperator,
    value: Union[str, List[str]],
    verified: bool = False
)
```

Use to select users by languages specified by the user in the profile.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`operator`|**[InclusionOperator](toloka.client.primitives.operators.InclusionOperator.md)**|<p>Comparison operator in the condition. For example, for a condition &quot;The user must be 18 years old or older» used date of birth and operator GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value</p>
`value`|**Union\[str, List\[str\]\]**|<p>Languages specified by the user in the profile (two-letter ISO code of the standard ISO 639-1 in upper case).</p>
`verified`|**-**|<p>If set to True only users who have passed language test will be selected. Currently only following ISO codes are supported: DE, EN, FR, JA, PT, SV, RU, AR, ES.</p>
