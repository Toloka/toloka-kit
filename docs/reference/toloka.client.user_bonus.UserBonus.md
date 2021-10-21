# UserBonus
`toloka.client.user_bonus.UserBonus`

```
UserBonus(
    self,
    *,
    user_id: Optional[str] = None,
    amount: Optional[Decimal] = None,
    private_comment: Optional[str] = None,
    public_title: Optional[Any] = None,
    public_message: Optional[Any] = None,
    without_message: Optional[bool] = None,
    assignment_id: Optional[str] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

Issuing a bonus to a specific performer


It's addition to payment for completed tasks.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`user_id`|**Optional\[str\]**|<p>Performer ID to whom the bonus will be issued.</p>
`amount`|**Optional\[Decimal\]**|<p>The bonus amount in dollars. Can be from 0.01 to 100 dollars per user per time.</p>
`private_comment`|**Optional\[str\]**|<p>Comments that are only visible to the requester.</p>
`public_title`|**Optional\[Any\]**|<p>Message header for the user. You can provide a title in several languages (the message will come in the user&#x27;s language).</p>
`public_message`|**Optional\[Any\]**|<p>Message text for the user. You can provide text in several languages (the message will come in the user&#x27;s language).</p>
`without_message`|**Optional\[bool\]**|<p>Do not send a bonus message to the user. To award a bonus without a message, specify null for public_title and public_message and True for without_message.</p>
`assignment_id`|**Optional\[str\]**|<p>The answer to the task for which this bonus was issued.</p>
`id`|**Optional\[str\]**|<p>Internal ID of the issued bonus. Read only.</p>
`created`|**Optional\[datetime\]**|<p>Date the bonus was awarded, in UTC. Read only.</p>

**Examples:**

How to create bonus with message for specific assignment.

```python
new_bonus = toloka_client.create_user_bonus(
    UserBonus(
        user_id='1',
        amount='0.50',
        public_title='Perfect job!',
        public_message='You are the best performer EVER!'
        assignment_id='012345'
    )
)
```

Hoiw to create bonus with message in several languages.

```python
new_bonus = toloka_client.create_user_bonus(
    UserBonus(
        user_id='1',
        amount='0.10',
        public_title= {
            'EN': 'Good Job!',
            'RU': 'Молодец!',
        },
        public_message: {
            'EN': 'Ten tasks completed',
            'RU': 'Выполнено 10 заданий',
        },
    )
)
```
