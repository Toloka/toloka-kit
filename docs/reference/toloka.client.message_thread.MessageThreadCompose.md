# MessageThreadCompose
`toloka.client.message_thread.MessageThreadCompose` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client/message_thread.py#L170)

```python
MessageThreadCompose(
    self,
    *,
    recipients_select_type: Union[RecipientsSelectType, str, None] = None,
    topic: Optional[Dict[str, str]] = None,
    text: Optional[Dict[str, str]] = None,
    answerable: Optional[bool] = None,
    recipients_ids: Optional[List[str]] = None,
    recipients_filter: Optional[FilterCondition] = None
)
```

Sent message to perfromer

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`recipients_select_type`|**Optional\[[RecipientsSelectType](toloka.client.message_thread.RecipientsSelectType.md)\]**|<p>Method for specifying recipients</p>
`topic`|**Optional\[Dict\[str, str\]\]**|<p>Post title. You can provide a title in several languages (the message will come in the user&#x27;s language). Format: &quot;&lt;language RU/EN/TR/ID/FR&gt;&quot;: &quot;&lt;topic text&gt;&quot;.</p>
`text`|**Optional\[Dict\[str, str\]\]**|<p>Message text. You can provide text in several languages (the message will come in the user&#x27;s language). Format: &quot;&lt;language RU/EN/TR/ID/FR&gt;&quot;: &quot;&lt;message text&gt;&quot;.</p>
`answerable`|**Optional\[bool\]**|<p>Ability to reply to a message:<ul><li>True — Users can respond to the message.</li><li>False — Users can&#x27;t respond to the message.</li></ul></p>
`recipients_ids`|**Optional\[List\[str\]\]**|<p>List of IDs of users to whom the message will be sent.</p>
`recipients_filter`|**Optional\[[FilterCondition](toloka.client.filter.FilterCondition.md)\]**|<p>Filter to select recipients.</p>
