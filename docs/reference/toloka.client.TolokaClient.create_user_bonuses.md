# create_user_bonuses
`toloka.client.TolokaClient.create_user_bonuses`

Creates many user bonuses


Right now it's safer to use asynchronous version: "create_user_bonuses_async"
You can send a maximum of 10,000 requests of this kind per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_bonuses`|**List\[[UserBonus](toloka.client.user_bonus.UserBonus.md)\]**|<p>To whom, how much to pay and for what.</p>
`operation_id`|**Optional\[str\]**|<p>Operation ID. If asynchronous creation is used, by this identifier you can later get results of creating bonuses.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters of objects:<ul><li>True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.</li><li>False - Default behaviour. Stop the operation and don&#x27;t award bonuses if at least one object didn&#x27;t pass validation.</li></ul></p>

* **Returns:**

  Result of user bonuses creating. Contains created user bonuses in `items` and
problems in "validation_errors".

* **Return type:**

  [UserBonusBatchCreateResult](toloka.client.batch_create_results.UserBonusBatchCreateResult.md)

**Examples:**

```python
import decimal
new_bonuses=[
    UserBonus(
        user_id='1',
        amount=decimal.Decimal('0.50'),
        public_title={
            'EN': 'Perfect job!',
            'RU': 'Прекрасная работа!',
        },
        public_message={
            'EN': 'You are the best performer!',
            'RU': 'Молодец!',
        },
        assignment_id='1'),
    UserBonus(
        user_id='2',
        amount=decimal.Decimal('1.0'),
        public_title={
            'EN': 'Excellent work!',
            'RU': 'Отличная работа!',
        },
        public_message={
            'EN': 'You have completed all tasks!',
            'RU': 'Сделаны все задания!',
        },
        assignment_id='2')
]
toloka_client.create_user_bonuses(new_bonuses)
```
