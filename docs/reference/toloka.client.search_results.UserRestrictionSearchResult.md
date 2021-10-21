# UserRestrictionSearchResult
`toloka.client.search_results.UserRestrictionSearchResult`

```
UserRestrictionSearchResult(
    self,
    *,
    items: Optional[List[UserRestriction]] = None,
    has_more: Optional[bool] = None
)
```

The list of found user restrictions and whether there is something else on the original request


It's better to use TolokaClient.get_user_restrictions(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[UserRestriction](toloka.client.user_restriction.UserRestriction.md)\]\]**|<p>List of found user restrictions</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
