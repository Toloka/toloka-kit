from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from .filter import FilterCondition
from .primitives.base import BaseTolokaObject


class RecipientsSelectType(Enum):
    ...

class Folder(Enum):
    """Folder where the thread is located.

    * INBOX — Inbox.
    * OUTBOX — Sent.
    * AUTOMATIC_NOTIFICATION — Notifications.
    * IMPORTANT — Important.
    * UNREAD — Unread.
    """
    ...

class Interlocutor(BaseTolokaObject):
    """Interlocutor

    Attributes:
        id: ID of the sender or recipient.
        role: Role of the sender or recipient in Toloka:
            * USER — Performer.
            * REQUESTER
            * ADMINISTRATOR
            * SYSTEM — For messages sent automatically.
        myself: Marks a sender or recipient with your ID. If this is your ID, it is set to true.
    """

    class InterlocutorRole(Enum):
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        id: Optional[str] = ...,
        role: Optional[InterlocutorRole] = ...,
        myself: Optional[bool] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    role: Optional[InterlocutorRole]
    myself: Optional[bool]

class MessageThread(BaseTolokaObject):
    """MessageThread

    Attributes:
        id: Message thread ID.
        topic: Message thread title.
        interlocutors_inlined: bool
        interlocutors: List[Interlocutor]
        messages_inlined: Access to message threads:
            * True — The message is available in the messages field.
            * False — The message is available in a separate request.
        messages: List[Message]
        meta: Meta
        answerable: Whether the message can be responded to:
            * True — The performer can respond to the message.
            * False — The performer cannot respond to the message.
        folders: Folders where the thread is located.
        compose_details: For messages that you sent: details of the POST request for creating the message.
        created: Date the first message in the thread was created.
    """

    class ComposeDetails(BaseTolokaObject):
        """For messages that you sent: details of the POST request for creating the message.

        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            recipients_select_type: Optional[RecipientsSelectType] = ...,
            recipients_ids: Optional[List[str]] = ...,
            recipients_filter: Optional[FilterCondition] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        recipients_select_type: Optional[RecipientsSelectType]
        recipients_ids: Optional[List[str]]
        recipients_filter: Optional[FilterCondition]

    class Meta(BaseTolokaObject):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            pool_id: Optional[str] = ...,
            project_id: Optional[str] = ...,
            assignment_id: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        pool_id: Optional[str]
        project_id: Optional[str]
        assignment_id: Optional[str]

    class Message(BaseTolokaObject):
        """Message in the thread.

        Attributes:
            text: Message text.
            from_: Information about the sender.
            created: Date the message was created.
        """

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            text: Optional[Dict[str, str]] = ...,
            from_: Optional[Interlocutor] = ...,
            created: Optional[datetime] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        text: Optional[Dict[str, str]]
        from_: Optional[Interlocutor]
        created: Optional[datetime]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        id: Optional[str] = ...,
        topic: Optional[Dict[str, str]] = ...,
        interlocutors_inlined: Optional[bool] = ...,
        interlocutors: Optional[List[Interlocutor]] = ...,
        messages_inlined: Optional[bool] = ...,
        messages: Optional[List[Message]] = ...,
        meta: Optional[Meta] = ...,
        answerable: Optional[bool] = ...,
        folders: Optional[List[Folder]] = ...,
        compose_details: Optional[ComposeDetails] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    id: Optional[str]
    topic: Optional[Dict[str, str]]
    interlocutors_inlined: Optional[bool]
    interlocutors: Optional[List[Interlocutor]]
    messages_inlined: Optional[bool]
    messages: Optional[List[Message]]
    meta: Optional[Meta]
    answerable: Optional[bool]
    folders: Optional[List[Folder]]
    compose_details: Optional[ComposeDetails]
    created: Optional[datetime]

class MessageThreadReply(BaseTolokaObject):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, text: Optional[Dict[str, str]] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    text: Optional[Dict[str, str]]

class MessageThreadFolders(BaseTolokaObject):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, folders: Optional[List[Folder]] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    folders: Optional[List[Folder]]

class MessageThreadCompose(BaseTolokaObject):
    """MessageThreadCompose

    Attributes:
        recipients_select_type: Method for selecting recipients
        topic: Subject of the message. You can enter the subject in multiple
            languages (the message is sent in the user's language). 
        text: Message text. You can enter the text in multiple languages (the message is sent in the user's language)
        answerable: Whether the message can be responded to:
            * True — Users can respond to the message.
            * False — Users can't respond to the message.
        recipients_ids: The list of IDs of users who will receive the message.
        recipients_filter: Filter for selecting recipients.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        recipients_select_type: Optional[RecipientsSelectType] = ...,
        topic: Optional[Dict[str, str]] = ...,
        text: Optional[Dict[str, str]] = ...,
        answerable: Optional[bool] = ...,
        recipients_ids: Optional[List[str]] = ...,
        recipients_filter: Optional[FilterCondition] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    recipients_select_type: Optional[RecipientsSelectType]
    topic: Optional[Dict[str, str]]
    text: Optional[Dict[str, str]]
    answerable: Optional[bool]
    recipients_ids: Optional[List[str]]
    recipients_filter: Optional[FilterCondition]
