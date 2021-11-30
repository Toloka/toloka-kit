# create_user_bonus
`toloka.client.TolokaClient.create_user_bonus`

Issues payments directly to the performer


You can send a maximum of 10,000 requests of this kind per day.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_bonus`|**[UserBonus](toloka.client.user_bonus.UserBonus.md)**|<p>To whom, how much to pay and for what.</p>
`operation_id`|**Optional\[str\]**|<p>Operation ID. If asynchronous creation is used, by this identifier you can later get results of creating bonuses.</p>
`skip_invalid_items`|**Optional\[bool\]**|<p>Validation parameters of objects:<ul><li>True - Award a bonus if the object with bonus information passed validation. Otherwise, skip the bonus.</li><li>False - Default behaviour. Stop the operation and don&#x27;t award bonuses if at least one object didn&#x27;t pass validation.</li></ul></p>

* **Returns:**

  Created bonus.

* **Return type:**

  [UserBonus](toloka.client.user_bonus.UserBonus.md)

**Examples:**

Create bonus for specific assignment.

```python
import decimal
new_bonus = toloka_client.create_user_bonus(
    UserBonus(
        user_id='1',
        amount=decimal.Decimal('0.50'),
        public_title='Perfect job!',
        public_message='You are the best performer!',
        assignment_id='012345'
    )
)
```
