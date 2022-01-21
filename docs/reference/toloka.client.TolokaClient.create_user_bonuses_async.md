# create_user_bonuses_async
`toloka.client.TolokaClient.create_user_bonuses_async`

Issues payments directly to the performers, asynchronously creates many user bonuses


You can send a maximum of 10,000 requests of this kind per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_bonuses`|**List\[[UserBonus](toloka.client.user_bonus.UserBonus.md)\]**|<p>To whom, how much to pay and for what.</p>
`operation_id`|**Optional\[str\]**|<p>Operation ID. If asynchronous creation is used, by this identifier you can later get results of creating bonuses.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters of objects:<ul><li>True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.</li><li>False - Default behaviour. Stop the operation and don&#x27;t award bonuses if at least one object didn&#x27;t pass validation.</li></ul></p>

* **Returns:**

  An operation upon completion of which the bonuses can be considered created.

* **Return type:**

  [UserBonusCreateBatchOperation](toloka.client.operations.UserBonusCreateBatchOperation.md)

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
            'RU': 'Превосходная работа!',
        },
        public_message={
            'EN': 'You have completed all tasks!',
            'RU': 'Сделаны все задания!',
        },
        assignment_id='2')
]
create_bonuses = toloka_client.create_user_bonuses_async(new_bonuses)
toloka_client.wait_operation(create_bonuses)
```
