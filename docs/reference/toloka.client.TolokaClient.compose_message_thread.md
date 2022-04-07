# compose_message_thread
`toloka.client.TolokaClient.compose_message_thread`

Sends message to performer


The sent message is added to a new message thread.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`recipients_select_type`|**Union\[[RecipientsSelectType](toloka.client.message_thread.RecipientsSelectType.md), str, None\]**|<p>Method for specifying recipients</p>
`topic`|**Optional\[Dict\[str, str\]\]**|<p>Post title. You can provide a title in several languages (the message will come in the user&#x27;s language). Format: &quot;&lt;language RU/EN/TR/ID/FR&gt;&quot;: &quot;&lt;topic text&gt;&quot;.</p>
`text`|**Optional\[Dict\[str, str\]\]**|<p>Message text. You can provide text in several languages (the message will come in the user&#x27;s language). Format: &quot;&lt;language RU/EN/TR/ID/FR&gt;&quot;: &quot;&lt;message text&gt;&quot;.</p>
`answerable`|**Optional\[bool\]**|<p>Ability to reply to a message:<ul><li>True — Users can respond to the message.</li><li>False — Users can&#x27;t respond to the message.</li></ul></p>
`recipients_ids`|**Optional\[List\[str\]\]**|<p>List of IDs of users to whom the message will be sent.</p>
`recipients_filter`|**Optional\[[FilterCondition](toloka.client.filter.FilterCondition.md)\]**|<p>Filter to select recipients.</p>

* **Returns:**

  New created thread.

* **Return type:**

  [MessageThread](toloka.client.message_thread.MessageThread.md)

**Examples:**

If you want to thank Toloka performers who have tried to complete your tasks, send them a nice message.

```python
message_text = "Amazing job! We've just trained our first model with the data YOU prepared for us. Thank you!"
toloka_client.compose_message_thread(
    recipients_select_type='ALL',
    topic={'EN': 'Thank you, performer!'},
    text={'EN': message_text},
    answerable=False
)
```
