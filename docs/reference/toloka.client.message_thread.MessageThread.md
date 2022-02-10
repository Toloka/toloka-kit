# MessageThread
`toloka.client.message_thread.MessageThread`

```python
MessageThread(
    self,
    *,
    id: Optional[str] = None,
    topic: Optional[Dict[str, str]] = None,
    interlocutors_inlined: Optional[bool] = None,
    interlocutors: Optional[List[Interlocutor]] = None,
    messages_inlined: Optional[bool] = None,
    messages: Optional[List[Message]] = None,
    meta: Optional[Meta] = None,
    answerable: Optional[bool] = None,
    folders: Optional[List[Folder]] = None,
    compose_details: Optional[ComposeDetails] = None,
    created: Optional[datetime] = None
)
```

Message thread.


The sent message is added to the new message thread. Until the first response is received the message chain is in
the folder UNREAD. If there are several addresses in the chain and one of them responds, a new message chain
will be created

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`id`|**Optional\[str\]**|<p>Message thread ID.</p>
`topic`|**Optional\[Dict\[str, str\]\]**|<p>Message thread title.</p>
`interlocutors_inlined`|**Optional\[bool\]**|<p>Access information about the sender and recipients.<ul><li>True - information is available in the field interlocutors.</li><li>False - information is available on a separate request.</li></ul></p>
`interlocutors`|**Optional\[List\[[Interlocutor](toloka.client.message_thread.Interlocutor.md)\]\]**|<p>Information about the sender and recipients, sorted by IDs.</p>
`messages_inlined`|**Optional\[bool\]**|<p>Access to message threads:<ul><li>True — The message is available in the messages field.</li><li>False — The message is available in a separate request.</li></ul></p>
`messages`|**Optional\[List\[[Message](toloka.client.message_thread.MessageThread.Message.md)\]\]**|<p>Messages in the thread. Sorted by creation date (new first).</p>
`meta`|**Optional\[[Meta](toloka.client.message_thread.MessageThread.Meta.md)\]**|<p>Meta</p>
`answerable`|**Optional\[bool\]**|<p>Ability to reply to a message:<ul><li>True — The performer can respond to the message.</li><li>False — The performer cannot respond to the message.</li></ul></p>
`folders`|**Optional\[List\[[Folder](toloka.client.message_thread.Folder.md)\]\]**|<p>Folders where the thread is located.</p>
`compose_details`|**Optional\[[ComposeDetails](toloka.client.message_thread.MessageThread.ComposeDetails.md)\]**|<p>For messages that you sent: details of the POST request for creating the message.</p>
`created`|**Optional\[datetime\]**|<p>The date the first message in the chain was created.</p>
