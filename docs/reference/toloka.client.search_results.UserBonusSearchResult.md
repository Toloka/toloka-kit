# UserBonusSearchResult
`toloka.client.search_results.UserBonusSearchResult`

```
UserBonusSearchResult(
    self,
    *,
    items: Optional[List[UserBonus]] = None,
    has_more: Optional[bool] = None
)
```

The list of found user bonuses and whether there is something else on the original request


It's better to use TolokaClient.get_user_bonuses(), which already implements the correct handling of the search result.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[List\[[UserBonus](toloka.client.user_bonus.UserBonus.md)\]\]**|<p>List of found user bonuses</p>
`has_more`|**Optional\[bool\]**|<p>Whether the list is complete:<ul><li>True - Not all elements are included in the output due to restrictions in the limit parameter.</li><li>False - The output lists all the items.</li></ul></p>
