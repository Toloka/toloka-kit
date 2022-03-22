# reply_message_thread
`toloka.client.TolokaClient.reply_message_thread` | [Source code](https://github.com/Toloka/toloka-kit/blob/v0.1.24/src/client.py#L44)

```python
reply_message_thread(
    self,
    message_thread_id: str,
    reply: MessageThreadReply
)
```

Replies to a message in thread

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`message_thread_id`|**str**|<p>In which thread to reply.</p>
`reply`|**[MessageThreadReply](toloka.client.message_thread.MessageThreadReply.md)**|<p>Reply message.</p>

* **Returns:**

  New created message.

* **Return type:**

  [MessageThread](toloka.client.message_thread.MessageThread.md)

**Examples:**

```python
message_threads = toloka_client.get_message_threads(folder='UNREAD')
message_reply = {'EN': 'Thank you for your message! I will get back to you soon.'}
for thread in message_threads:
    toloka_client.reply_message_thread(message_thread_id=thread.id, reply=toloka.message_thread.MessageThreadReply(text=message_reply))
```
