# ComposeDetails
`toloka.client.message_thread.MessageThread.ComposeDetails` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.25/src/client/message_thread.py#L102)

```python
ComposeDetails(
    self,
    *,
    recipients_select_type: Union[RecipientsSelectType, str, None] = None,
    recipients_ids: Optional[List[str]] = None,
    recipients_filter: Optional[FilterCondition] = None
)
```

For messages that you sent: details of the POST request for creating the message.

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`recipients_select_type`|**Optional\[[RecipientsSelectType](toloka.client.message_thread.RecipientsSelectType.md)\]**|<p>Method for specifying recipients.</p>
`recipients_ids`|**Optional\[List\[str\]\]**|<p>List of recipients IDs.</p>
`recipients_filter`|**Optional\[[FilterCondition](toloka.client.filter.FilterCondition.md)\]**|<p>Condition to filter recipients.</p>
