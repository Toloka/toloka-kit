# UserBonusBatchCreateResult
`toloka.client.batch_create_results.UserBonusBatchCreateResult`

```
UserBonusBatchCreateResult(
    self,
    *,
    items: Optional[Dict[str, UserBonus]] = None,
    validation_errors: Optional[Dict[str, Dict[str, FieldValidationError]]] = None
)
```

The list with the results of the user bonuses creation operation.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`items`|**Optional\[Dict\[str, [UserBonus](toloka.client.user_bonus.UserBonus.md)\]\]**|<p>Object with information about issued bonuses.</p>
`validation_errors`|**Optional\[Dict\[str, Dict\[str, [FieldValidationError](toloka.client.batch_create_results.FieldValidationError.md)\]\]\]**|<p>Object with validation errors. Returned if the parameter is used in the request skip_invalid_items=True.</p>
